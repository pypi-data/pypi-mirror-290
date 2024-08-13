import asyncio
from functools import partial
from typing import get_args
from unittest import mock

import faker
import pytest

import stompman.subscription
from stompman import (
    AckFrame,
    AckMode,
    ConnectedFrame,
    ErrorFrame,
    FailedAllConnectAttemptsError,
    HeartbeatFrame,
    MessageFrame,
    NackFrame,
    ReceiptFrame,
    SendFrame,
    SubscribeFrame,
    UnsubscribeFrame,
)
from tests.conftest import (
    CONNECT_FRAME,
    CONNECTED_FRAME,
    EnrichedClient,
    SomeError,
    build_dataclass,
    create_spying_connection,
    enrich_expected_frames,
    get_read_frames_with_lifespan,
    noop_error_handler,
    noop_message_handler,
)

pytestmark = pytest.mark.anyio
FAKER = faker.Faker()


@pytest.mark.parametrize("ack", get_args(AckMode))
async def test_client_subscribtions_lifespan_resubscribe(ack: AckMode) -> None:
    connection_class, collected_frames = create_spying_connection(*get_read_frames_with_lifespan([CONNECTED_FRAME], []))
    client = EnrichedClient(connection_class=connection_class)
    sub_destination, message_destination, message_body = FAKER.pystr(), FAKER.pystr(), FAKER.binary(length=10)

    async with client:
        subscription = await client.subscribe(
            destination=sub_destination,
            handler=noop_message_handler,
            ack=ack,
            on_suppressed_exception=noop_error_handler,
        )
        client._connection_manager._clear_active_connection_state()
        await client.send(message_body, destination=message_destination)
        await subscription.unsubscribe()
        await asyncio.sleep(0)
        await asyncio.sleep(0)

    assert collected_frames == enrich_expected_frames(
        SubscribeFrame(headers={"id": subscription.id, "destination": sub_destination, "ack": ack}),
        CONNECT_FRAME,
        CONNECTED_FRAME,
        SubscribeFrame(headers={"id": subscription.id, "destination": sub_destination, "ack": ack}),
        SendFrame(
            headers={"destination": message_destination, "content-length": str(len(message_body))}, body=message_body
        ),
        UnsubscribeFrame(headers={"id": subscription.id}),
    )


async def test_client_subscribtions_lifespan_no_active_subs_in_aexit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        stompman.subscription,
        "_make_subscription_id",
        mock.Mock(side_effect=[(first_id := FAKER.pystr()), (second_id := FAKER.pystr())]),
    )
    first_destination, second_destination = FAKER.pystr(), FAKER.pystr()
    connection_class, collected_frames = create_spying_connection(*get_read_frames_with_lifespan([]))

    async with EnrichedClient(connection_class=connection_class) as client:
        first_subscription = await client.subscribe(
            first_destination, handler=noop_message_handler, on_suppressed_exception=noop_error_handler
        )
        second_subscription = await client.subscribe(
            second_destination, handler=noop_message_handler, on_suppressed_exception=noop_error_handler
        )
        await asyncio.sleep(0)
        await first_subscription.unsubscribe()
        await second_subscription.unsubscribe()

    assert collected_frames == enrich_expected_frames(
        SubscribeFrame(headers={"id": first_id, "destination": first_destination, "ack": "client-individual"}),
        SubscribeFrame(headers={"id": second_id, "destination": second_destination, "ack": "client-individual"}),
        UnsubscribeFrame(headers={"id": first_id}),
        UnsubscribeFrame(headers={"id": second_id}),
    )


@pytest.mark.parametrize("direct_error", [True, False])
async def test_client_subscribtions_lifespan_with_active_subs_in_aexit(
    monkeypatch: pytest.MonkeyPatch,
    *,
    direct_error: bool,
) -> None:
    subscription_id, destination = FAKER.pystr(), FAKER.pystr()
    monkeypatch.setattr(stompman.subscription, "_make_subscription_id", mock.Mock(return_value=subscription_id))
    connection_class, collected_frames = create_spying_connection(*get_read_frames_with_lifespan([]))

    if direct_error:
        with pytest.raises(SomeError):  # noqa: PT012
            async with EnrichedClient(connection_class=connection_class) as client:
                await client.subscribe(
                    destination, handler=noop_message_handler, on_suppressed_exception=noop_error_handler
                )
                await SomeError.raise_after_tick()
    else:
        with pytest.raises(ExceptionGroup) as exc_info:  # noqa: PT012
            async with asyncio.TaskGroup() as task_group, EnrichedClient(connection_class=connection_class) as client:
                await client.subscribe(
                    destination, handler=noop_message_handler, on_suppressed_exception=noop_error_handler
                )
                task_group.create_task(SomeError.raise_after_tick())

        assert exc_info.value.exceptions == (SomeError(),)

    assert collected_frames == enrich_expected_frames(
        SubscribeFrame(headers={"id": subscription_id, "destination": destination, "ack": "client-individual"}),
        UnsubscribeFrame(headers={"id": subscription_id}),
    )


async def test_client_listen_routing_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        stompman.subscription,
        "_make_subscription_id",
        mock.Mock(side_effect=[(first_sub_id := FAKER.pystr()), (second_sub_id := FAKER.pystr())]),
    )
    connection_class, _ = create_spying_connection(
        *get_read_frames_with_lifespan(
            [
                build_dataclass(ConnectedFrame),
                build_dataclass(ReceiptFrame),
                (first_message_frame := build_dataclass(MessageFrame, headers={"subscription": first_sub_id})),
                (error_frame := build_dataclass(ErrorFrame)),
                (_second_message_frame := build_dataclass(MessageFrame)),
                (third_message_frame := build_dataclass(MessageFrame, headers={"subscription": second_sub_id})),
                HeartbeatFrame(),
            ]
        )
    )
    first_message_handler, first_error_handler = mock.AsyncMock(return_value=None), mock.Mock()
    second_message_handler, second_error_handler = mock.AsyncMock(side_effect=SomeError), mock.Mock()

    async with EnrichedClient(
        connection_class=connection_class,
        on_error_frame=(on_error_frame := mock.Mock()),
        on_heartbeat=(on_heartbeat := mock.Mock()),
    ) as client:
        first_subscription = await client.subscribe(
            FAKER.pystr(), handler=first_message_handler, on_suppressed_exception=first_error_handler
        )
        second_subscription = await client.subscribe(
            FAKER.pystr(), handler=second_message_handler, on_suppressed_exception=second_error_handler
        )
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await first_subscription.unsubscribe()
        await second_subscription.unsubscribe()

    first_message_handler.assert_called_once_with(first_message_frame)
    first_error_handler.assert_not_called()

    second_message_handler.assert_called_once_with(third_message_frame)
    second_error_handler.assert_called_once_with(SomeError(), third_message_frame)

    on_error_frame.assert_called_once_with(error_frame)
    on_heartbeat.assert_called_once_with()


@pytest.mark.parametrize("side_effect", [None, SomeError])
@pytest.mark.parametrize("ack", ["client", "client-individual"])
async def test_client_listen_unsubscribe_before_ack_or_nack(
    monkeypatch: pytest.MonkeyPatch, ack: AckMode, side_effect: object
) -> None:
    subscription_id, destination = FAKER.pystr(), FAKER.pystr()
    monkeypatch.setattr(stompman.subscription, "_make_subscription_id", mock.Mock(return_value=subscription_id))

    message_frame = build_dataclass(MessageFrame, headers={"subscription": subscription_id})
    connection_class, collected_frames = create_spying_connection(*get_read_frames_with_lifespan([message_frame]))
    message_handler = mock.AsyncMock(side_effect=side_effect)

    async with EnrichedClient(connection_class=connection_class) as client:
        subscription = await client.subscribe(
            destination, message_handler, on_suppressed_exception=noop_error_handler, ack=ack
        )
        await asyncio.sleep(0)
        await subscription.unsubscribe()
        await asyncio.sleep(0)

    message_handler.assert_called_once_with(message_frame)
    assert collected_frames == enrich_expected_frames(
        SubscribeFrame(headers={"ack": ack, "destination": destination, "id": subscription_id}),
        message_frame,
        UnsubscribeFrame(headers={"id": subscription_id}),
    )


@pytest.mark.parametrize("ok", [True, False])
@pytest.mark.parametrize("ack", ["client", "client-individual"])
async def test_client_listen_ack_nack_sent(monkeypatch: pytest.MonkeyPatch, ack: AckMode, *, ok: bool) -> None:
    subscription_id, destination, message_id = FAKER.pystr(), FAKER.pystr(), FAKER.pystr()
    monkeypatch.setattr(stompman.subscription, "_make_subscription_id", mock.Mock(return_value=subscription_id))

    message_frame = build_dataclass(
        MessageFrame, headers={"destination": destination, "message-id": message_id, "subscription": subscription_id}
    )
    connection_class, collected_frames = create_spying_connection(*get_read_frames_with_lifespan([message_frame]))
    message_handler = mock.AsyncMock(side_effect=None if ok else SomeError)

    async with EnrichedClient(connection_class=connection_class) as client:
        subscription = await client.subscribe(
            destination, message_handler, on_suppressed_exception=noop_error_handler, ack=ack
        )
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await subscription.unsubscribe()

    message_handler.assert_called_once_with(message_frame)
    assert collected_frames == enrich_expected_frames(
        SubscribeFrame(headers={"id": subscription_id, "destination": destination, "ack": ack}),
        message_frame,
        AckFrame(headers={"id": message_id, "subscription": subscription_id})
        if ok
        else NackFrame(headers={"id": message_id, "subscription": subscription_id}),
        UnsubscribeFrame(headers={"id": subscription_id}),
    )


@pytest.mark.parametrize("ok", [True, False])
async def test_client_listen_auto_ack_nack(monkeypatch: pytest.MonkeyPatch, *, ok: bool) -> None:
    subscription_id, destination, message_id = FAKER.pystr(), FAKER.pystr(), FAKER.pystr()
    monkeypatch.setattr(stompman.subscription, "_make_subscription_id", mock.Mock(return_value=subscription_id))

    message_frame = build_dataclass(
        MessageFrame, headers={"destination": destination, "message-id": message_id, "subscription": subscription_id}
    )
    connection_class, collected_frames = create_spying_connection(*get_read_frames_with_lifespan([message_frame]))
    message_handler = mock.AsyncMock(side_effect=None if ok else SomeError)

    async with EnrichedClient(connection_class=connection_class) as client:
        subscription = await client.subscribe(
            destination, message_handler, on_suppressed_exception=noop_error_handler, ack="auto"
        )
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await subscription.unsubscribe()

    message_handler.assert_called_once_with(message_frame)
    assert collected_frames == enrich_expected_frames(
        SubscribeFrame(headers={"ack": "auto", "destination": destination, "id": subscription_id}),
        message_frame,
        UnsubscribeFrame(headers={"id": subscription_id}),
    )


async def test_client_listen_raises_on_aexit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("asyncio.sleep", partial(asyncio.sleep, 0))

    connection_class, _ = create_spying_connection(*get_read_frames_with_lifespan([]))
    connection_class.connect = mock.AsyncMock(side_effect=[connection_class(), None, None, None])  # type: ignore[method-assign]

    async def close_connection_soon(client: stompman.Client) -> None:
        await asyncio.sleep(0)
        client._connection_manager._clear_active_connection_state()

    with pytest.raises(ExceptionGroup) as exc_info:  # noqa: PT012
        async with asyncio.TaskGroup() as task_group, EnrichedClient(connection_class=connection_class) as client:
            await client.subscribe(FAKER.pystr(), noop_message_handler, on_suppressed_exception=noop_error_handler)
            task_group.create_task(close_connection_soon(client))

    assert len(exc_info.value.exceptions) == 1
    inner_group = exc_info.value.exceptions[0]

    assert isinstance(inner_group, ExceptionGroup)
    assert len(inner_group.exceptions) == 1

    assert isinstance(inner_group.exceptions[0], FailedAllConnectAttemptsError)


def test_make_subscription_id() -> None:
    stompman.subscription._make_subscription_id()
