from typing import Union, Optional, Any, Literal, IO, BinaryIO
import time
from datetime import datetime
from dataclasses import is_dataclass
import secrets
from http import HTTPStatus

from requests import Session, Response, RequestException
from requests_toolbelt import MultipartEncoder

from telebox.bot.utils.converters import DataclassConverter, get_timestamp
from telebox.bot.errors import get_request_error, BotError, RetryAfterError, InternalServerError
from telebox.bot.consts import chat_member_statuses
from telebox.bot.types.types.response_parameters import ResponseParameters
from telebox.bot.types.types.update import Update
from telebox.bot.types.types.webhook_info import WebhookInfo
from telebox.bot.types.types.user import User
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.bot.types.types.reply_keyboard_remove import ReplyKeyboardRemove
from telebox.bot.types.types.force_reply import ForceReply
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.message_id import MessageId
from telebox.bot.types.types.input_media import InputMedia
from telebox.bot.types.types.input_media_audio import InputMediaAudio
from telebox.bot.types.types.input_media_document import InputMediaDocument
from telebox.bot.types.types.input_media_photo import InputMediaPhoto
from telebox.bot.types.types.input_media_video import InputMediaVideo
from telebox.bot.types.types.user_profile_photos import UserProfilePhotos
from telebox.bot.types.types.chat_permissions import ChatPermissions
from telebox.bot.types.types.file import File
from telebox.bot.types.types.chat_invite_link import ChatInviteLink
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.bot_command import BotCommand
from telebox.bot.types.types.bot_command_scope import BotCommandScope
from telebox.bot.types.types.bot_description import BotDescription
from telebox.bot.types.types.bot_name import BotName
from telebox.bot.types.types.bot_short_description import BotShortDescription
from telebox.bot.types.types.menu_button import MenuButton
from telebox.bot.types.types.chat_administrator_rights import ChatAdministratorRights
from telebox.bot.types.types.forum_topic import ForumTopic
from telebox.bot.types.types.poll import Poll
from telebox.bot.types.types.sticker import Sticker
from telebox.bot.types.types.sticker_set import StickerSet
from telebox.bot.types.types.mask_position import MaskPosition
from telebox.bot.types.types.input_sticker import InputSticker
from telebox.bot.types.types.inline_query_result import InlineQueryResult
from telebox.bot.types.types.sent_web_app_message import SentWebAppMessage
from telebox.bot.types.types.labeled_price import LabeledPrice
from telebox.bot.types.types.shipping_option import ShippingOption
from telebox.bot.types.types.passport_element_error import PassportElementError
from telebox.bot.types.types.game_high_score import GameHighScore
from telebox.bot.types.types.chat_member import ChatMember
from telebox.bot.types.types.chat_member_owner import ChatMemberOwner
from telebox.bot.types.types.chat_member_administrator import ChatMemberAdministrator
from telebox.bot.types.types.chat_member_member import ChatMemberMember
from telebox.bot.types.types.chat_member_restricted import ChatMemberRestricted
from telebox.bot.types.types.chat_member_left import ChatMemberLeft
from telebox.bot.types.types.chat_member_banned import ChatMemberBanned
from telebox.bot.types.types.inline_query_results_button import InlineQueryResultsButton
from telebox.bot.types.types.reaction_type import ReactionType
from telebox.bot.types.types.reply_parameters import ReplyParameters
from telebox.bot.types.types.link_preview_options import LinkPreviewOptions
from telebox.bot.types.types.user_chat_boosts import UserChatBoosts
from telebox.utils.not_set import NotSet, NOT_SET
from telebox.utils.serialization import get_serialized_data


API_URL = "https://api.telegram.org"
_CHAT_MEMBER_TYPES = {
    chat_member_statuses.CREATOR: ChatMemberOwner,
    chat_member_statuses.ADMINISTRATOR: ChatMemberAdministrator,
    chat_member_statuses.MEMBER: ChatMemberMember,
    chat_member_statuses.RESTRICTED: ChatMemberRestricted,
    chat_member_statuses.LEFT: ChatMemberLeft,
    chat_member_statuses.KICKED: ChatMemberBanned
}


class Bot:

    def __init__(
        self,
        session: Session,
        token: str,
        *,
        api_url: str = API_URL,
        parse_mode: Union[str, NotSet] = NOT_SET,
        timeout_secs: Union[int, float, None] = 300,
        retries: int = 0,
        retry_delay_secs: Union[int, float] = 0,
        wait_on_rate_limit: bool = False
    ):
        if retries < 0:
            raise ValueError("Number of retries cannot be less than zero!")

        self.session = session
        self.token = token
        self.api_url = api_url.lower().rstrip("/")
        self._parse_mode = parse_mode
        self._timeout_secs = timeout_secs
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._wait_on_rate_limit = wait_on_rate_limit
        self._dataclass_converter = DataclassConverter()
        self._me: Optional[User] = None

    @property
    def me(self) -> User:
        if self._me is None:
            raise BotError(
                "Bot user was not loaded! To use this property, you need to call "
                "bot.get_me method at least once!"
            )

        return self._me

    def get_updates(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[list[str]] = None
    ) -> list[Update]:
        return [
            self._dataclass_converter.get_object(data=i, class_=Update)
            for i in self._send_request(
                method="getUpdates",
                parameters={
                    "offset": offset,
                    "limit": limit,
                    "timeout": timeout,
                    "allowed_updates": allowed_updates
                },
                timeout_secs=timeout_secs
            )
        ]

    def set_webhook(
        self,
        url: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        certificate: Optional[InputFile] = None,
        ip_address: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[list[str]] = None,
        drop_pending_updates: Optional[bool] = None,
        secret_token: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setWebhook",
            parameters={
                "url": url,
                "certificate": certificate,
                "ip_address": ip_address,
                "max_connections": max_connections,
                "allowed_updates": allowed_updates,
                "drop_pending_updates": drop_pending_updates,
                "secret_token": secret_token
            },
            timeout_secs=timeout_secs
        )

    def delete_webhook(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        drop_pending_updates: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteWebhook",
            parameters={
                "drop_pending_updates": drop_pending_updates
            },
            timeout_secs=timeout_secs
        )

    def get_webhook_info(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> WebhookInfo:
        return self._dataclass_converter.get_object(
            data=self._send_request(method="getWebhookInfo", timeout_secs=timeout_secs),
            class_=WebhookInfo
        )

    def get_me(self, *, timeout_secs: Union[int, float, None] = None) -> User:
        self._me = self._dataclass_converter.get_object(
            data=self._send_request(method="getMe", timeout_secs=timeout_secs),
            class_=User
        )

        return self._me

    def log_out(self, *, timeout_secs: Union[int, float, None] = None) -> Literal[True]:
        return self._send_request(method="logOut", timeout_secs=timeout_secs)

    def close(self, *, timeout_secs: Union[int, float, None] = None) -> Literal[True]:
        return self._send_request(method="close", timeout_secs=timeout_secs)

    def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        entities: Optional[list[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendMessage",
                parameters={
                    "chat_id": chat_id,
                    "text": text,
                    "message_thread_id": message_thread_id,
                    "parse_mode": self._get_parse_mode(parse_mode, with_entities=bool(entities)),
                    "entities": entities,
                    "link_preview_options": link_preview_options,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="forwardMessage",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_id": message_id,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def forward_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: list[int],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> list[MessageId]:
        return [
            self._dataclass_converter.get_object(data=i, class_=MessageId)
            for i in self._send_request(
                method="forwardMessages",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_ids": message_ids,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content
                },
                timeout_secs=timeout_secs
            )
        ]

    def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> MessageId:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="copyMessage",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_id": message_id,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=MessageId
        )

    def copy_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: list[int],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        remove_caption: Optional[bool] = None
    ) -> list[MessageId]:
        return [
            self._dataclass_converter.get_object(data=i, class_=MessageId)
            for i in self._send_request(
                method="copyMessages",
                parameters={
                    "chat_id": chat_id,
                    "from_chat_id": from_chat_id,
                    "message_ids": message_ids,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "remove_caption": remove_caption
                },
                timeout_secs=timeout_secs
            )
        ]

    def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendPhoto",
                parameters={
                    "chat_id": chat_id,
                    "photo": photo,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "has_spoiler": has_spoiler,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendAudio",
                parameters={
                    "chat_id": chat_id,
                    "audio": audio,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "duration": duration,
                    "performer": performer,
                    "title": title,
                    "thumbnail": thumbnail,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendDocument",
                parameters={
                    "chat_id": chat_id,
                    "document": document,
                    "message_thread_id": message_thread_id,
                    "thumbnail": thumbnail,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "disable_content_type_detection": disable_content_type_detection,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendVideo",
                parameters={
                    "chat_id": chat_id,
                    "video": video,
                    "message_thread_id": message_thread_id,
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "thumbnail": thumbnail,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "has_spoiler": has_spoiler,
                    "supports_streaming": supports_streaming,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendAnimation",
                parameters={
                    "chat_id": chat_id,
                    "animation": animation,
                    "message_thread_id": message_thread_id,
                    "duration": duration,
                    "width": width,
                    "height": height,
                    "thumbnail": thumbnail,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "has_spoiler": has_spoiler,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendVoice",
                parameters={
                    "chat_id": chat_id,
                    "voice": voice,
                    "message_thread_id": message_thread_id,
                    "caption": caption,
                    "parse_mode": self._get_parse_mode(
                        parse_mode,
                        with_entities=bool(caption_entities)
                    ),
                    "caption_entities": caption_entities,
                    "duration": duration,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_video_note(
        self,
        chat_id: Union[int, str],
        video_note: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Union[InputFile, str, None] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendVideoNote",
                parameters={
                    "chat_id": chat_id,
                    "video_note": video_note,
                    "message_thread_id": message_thread_id,
                    "duration": duration,
                    "length": length,
                    "thumbnail": thumbnail,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_media_group(
        self,
        chat_id: Union[int, str],
        media: list[Union[InputMediaAudio,
                          InputMediaDocument,
                          InputMediaPhoto,
                          InputMediaVideo]],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None
    ) -> list[Message]:
        return [
            self._dataclass_converter.get_object(data=i, class_=Message)
            for i in self._send_request(
                method="sendMediaGroup",
                parameters={
                    "chat_id": chat_id,
                    "media": media,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters
                },
                timeout_secs=timeout_secs
            )
        ]

    def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendLocation",
                parameters={
                    "chat_id": chat_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "message_thread_id": message_thread_id,
                    "horizontal_accuracy": horizontal_accuracy,
                    "live_period": live_period,
                    "heading": heading,
                    "proximity_alert_radius": proximity_alert_radius,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageLiveLocation",
            parameters={
                "latitude": latitude,
                "longitude": longitude,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "horizontal_accuracy": horizontal_accuracy,
                "heading": heading,
                "proximity_alert_radius": proximity_alert_radius,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def stop_message_live_location(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="stopMessageLiveLocation",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def send_venue(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendVenue",
                parameters={
                    "chat_id": chat_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "title": title,
                    "address": address,
                    "message_thread_id": message_thread_id,
                    "foursquare_id": foursquare_id,
                    "foursquare_type": foursquare_type,
                    "google_place_id": google_place_id,
                    "google_place_type": google_place_type,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendContact",
                parameters={
                    "chat_id": chat_id,
                    "phone_number": phone_number,
                    "first_name": first_name,
                    "message_thread_id": message_thread_id,
                    "last_name": last_name,
                    "vcard": vcard,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: list[str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        is_anonymous: Optional[bool] = None,
        type_: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Union[str, None, NotSet] = NOT_SET,
        explanation_entities: Optional[list[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[datetime] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendPoll",
                parameters={
                    "chat_id": chat_id,
                    "question": question,
                    "options": options,
                    "message_thread_id": message_thread_id,
                    "is_anonymous": is_anonymous,
                    "type": type_,
                    "allows_multiple_answers": allows_multiple_answers,
                    "correct_option_id": correct_option_id,
                    "explanation": explanation,
                    "explanation_parse_mode": self._get_parse_mode(
                        explanation_parse_mode,
                        with_entities=bool(explanation_entities)
                    ),
                    "explanation_entities": explanation_entities,
                    "open_period": open_period,
                    "close_date": close_date,
                    "is_closed": is_closed,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_dice(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendDice",
                parameters={
                    "chat_id": chat_id,
                    "message_thread_id": message_thread_id,
                    "emoji": emoji,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def send_chat_action(
        self,
        chat_id: Union[int, str],
        action: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None
    ) -> Literal[True]:
        return self._send_request(
            method="sendChatAction",
            parameters={
                "chat_id": chat_id,
                "action": action,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def set_message_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        reaction: Optional[list[ReactionType]] = None,
        is_big: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMessageReaction",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "reaction": reaction,
                "is_big": is_big
            },
            timeout_secs=timeout_secs
        )

    def get_user_profile_photos(
        self,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> UserProfilePhotos:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getUserProfilePhotos",
                parameters={
                    "user_id": user_id,
                    "offset": offset,
                    "limit": limit
                },
                timeout_secs=timeout_secs
            ),
            class_=UserProfilePhotos
        )

    def get_file(
        self,
        file_id: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> File:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getFile",
                parameters={
                    "file_id": file_id
                },
                timeout_secs=timeout_secs
            ),
            class_=File
        )

    def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        until_date: Optional[datetime] = None,
        revoke_messages: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="banChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "until_date": until_date,
                "revoke_messages": revoke_messages
            },
            timeout_secs=timeout_secs
        )

    def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        only_if_banned: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unbanChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "only_if_banned": only_if_banned
            },
            timeout_secs=timeout_secs
        )

    def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: ChatPermissions,
        *,
        timeout_secs: Union[int, float, None] = None,
        use_independent_chat_permissions: Optional[bool] = None,
        until_date: Optional[datetime] = None
    ) -> Literal[True]:
        return self._send_request(
            method="restrictChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "permissions": permissions,
                "use_independent_chat_permissions": use_independent_chat_permissions,
                "until_date": until_date
            },
            timeout_secs=timeout_secs
        )

    def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_post_stories: Optional[bool] = None,
        can_edit_stories: Optional[bool] = None,
        can_delete_stories: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="promoteChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "is_anonymous": is_anonymous,
                "can_manage_chat": can_manage_chat,
                "can_post_messages": can_post_messages,
                "can_edit_messages": can_edit_messages,
                "can_delete_messages": can_delete_messages,
                "can_manage_video_chats": can_manage_video_chats,
                "can_restrict_members": can_restrict_members,
                "can_promote_members": can_promote_members,
                "can_change_info": can_change_info,
                "can_invite_users": can_invite_users,
                "can_pin_messages": can_pin_messages,
                "can_post_stories": can_post_stories,
                "can_edit_stories": can_edit_stories,
                "can_delete_stories": can_delete_stories,
                "can_manage_topics": can_manage_topics
            },
            timeout_secs=timeout_secs
        )

    def set_chat_administrator_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: int,
        custom_title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatAdministratorCustomTitle",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id,
                "custom_title": custom_title
            },
            timeout_secs=timeout_secs
        )

    def ban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="banChatSenderChat",
            parameters={
                "chat_id": chat_id,
                "sender_chat_id": sender_chat_id
            },
            timeout_secs=timeout_secs
        )

    def unban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unbanChatSenderChat",
            parameters={
                "chat_id": chat_id,
                "sender_chat_id": sender_chat_id
            },
            timeout_secs=timeout_secs
        )

    def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: ChatPermissions,
        *,
        timeout_secs: Union[int, float, None] = None,
        use_independent_chat_permissions: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatPermissions",
            parameters={
                "chat_id": chat_id,
                "permissions": permissions,
                "use_independent_chat_permissions": use_independent_chat_permissions
            },
            timeout_secs=timeout_secs
        )

    def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> str:
        return self._send_request(
            method="exportChatInviteLink",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="createChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "name": name,
                    "expire_date": expire_date,
                    "member_limit": member_limit,
                    "creates_join_request": creates_join_request
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatInviteLink
        )

    def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        expire_date: Optional[datetime] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> ChatInviteLink:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="editChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "invite_link": invite_link,
                    "name": name,
                    "expire_date": expire_date,
                    "member_limit": member_limit,
                    "creates_join_request": creates_join_request
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatInviteLink
        )

    def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatInviteLink:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="revokeChatInviteLink",
                parameters={
                    "chat_id": chat_id,
                    "invite_link": invite_link
                },
                timeout_secs=timeout_secs
            ),
            class_=ChatInviteLink
        )

    def approve_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="approveChatJoinRequest",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout_secs=timeout_secs
        )

    def decline_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="declineChatJoinRequest",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout_secs=timeout_secs
        )

    def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: InputFile,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatPhoto",
            parameters={
                "chat_id": chat_id,
                "photo": photo
            },
            timeout_secs=timeout_secs
        )

    def delete_chat_photo(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteChatPhoto",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )
    
    def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatTitle",
            parameters={
                "chat_id": chat_id,
                "title": title
            },
            timeout_secs=timeout_secs
        )

    def set_chat_description(
        self,
        chat_id: Union[int, str],
        description: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatDescription",
            parameters={
                "chat_id": chat_id,
                "description": description
            },
            timeout_secs=timeout_secs
        )

    def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        disable_notification: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="pinChatMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "disable_notification": disable_notification
            },
            timeout_secs=timeout_secs
        )

    def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinChatMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id
            },
            timeout_secs=timeout_secs
        )

    def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None,
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllChatMessages",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def leave_chat(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="leaveChat",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def get_chat(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Chat:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getChat",
                parameters={
                    "chat_id": chat_id
                },
                timeout_secs=timeout_secs
            ),
            class_=Chat
        )

    def get_chat_administrators(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Union[ChatMemberOwner,
                    ChatMemberAdministrator]]:
        return [
            self._dataclass_converter.get_object(data=i, class_=_CHAT_MEMBER_TYPES[i["status"]])
            for i in self._send_request(
                method="getChatAdministrators",
                parameters={
                    "chat_id": chat_id
                },
                timeout_secs=timeout_secs
            )
        ]

    def get_chat_member_count(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> int:
        return self._send_request(
            method="getChatMemberCount",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> ChatMember:
        data = self._send_request(
            method="getChatMember",
            parameters={
                "chat_id": chat_id,
                "user_id": user_id
            },
            timeout_secs=timeout_secs
        )

        return self._dataclass_converter.get_object(
            data=data,
            class_=_CHAT_MEMBER_TYPES[data["status"]]
        )

    def set_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        sticker_set_name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatStickerSet",
            parameters={
                "chat_id": chat_id,
                "sticker_set_name": sticker_set_name
            },
            timeout_secs=timeout_secs
        )

    def delete_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteChatStickerSet",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def get_forum_topic_icon_stickers(
        self,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Sticker]:
        return [
            self._dataclass_converter.get_object(data=i, class_=Sticker)
            for i in self._send_request(
                method="getForumTopicIconStickers",
                timeout_secs=timeout_secs
            )
        ]

    def create_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> ForumTopic:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="createForumTopic",
                parameters={
                    "chat_id": chat_id,
                    "name": name,
                    "icon_color": icon_color,
                    "icon_custom_emoji_id": icon_custom_emoji_id
                },
                timeout_secs=timeout_secs
            ),
            class_=ForumTopic
        )

    def edit_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="editForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id,
                "name": name,
                "icon_custom_emoji_id": icon_custom_emoji_id
            },
            timeout_secs=timeout_secs
        )

    def close_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="closeForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def reopen_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="reopenForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )
    
    def delete_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteForumTopic",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def unpin_all_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllForumTopicMessages",
            parameters={
                "chat_id": chat_id,
                "message_thread_id": message_thread_id
            },
            timeout_secs=timeout_secs
        )

    def edit_general_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="editGeneralForumTopic",
            parameters={
                "chat_id": chat_id,
                "name": name
            },
            timeout_secs=timeout_secs
        )

    def close_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="closeGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def reopen_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="reopenGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def hide_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="hideGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def unhide_general_forum_topic(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unhideGeneralForumTopic",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def unpin_all_general_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="unpinAllGeneralForumTopicMessages",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def answer_callback_query(
        self,
        callback_query_id: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerCallbackQuery",
            parameters={
                "callback_query_id": callback_query_id,
                "text": text,
                "show_alert": show_alert,
                "url": url,
                "cache_time": cache_time
            },
            timeout_secs=timeout_secs
        )

    def get_user_chat_boosts(
        self,
        chat_id: int,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> UserChatBoosts:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getUserChatBoosts",
                parameters={
                    "chat_id": chat_id,
                    "user_id": user_id
                },
                timeout_secs=timeout_secs
            ),
            class_=UserChatBoosts
        )

    def set_my_commands(
        self,
        commands: list[BotCommand],
        *,
        timeout_secs: Union[int, float, None] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyCommands",
            parameters={
                "commands": commands,
                "scope": scope,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def delete_my_commands(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMyCommands",
            parameters={
                "scope": scope,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_commands(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None
    ) -> list[BotCommand]:
        return [
            self._dataclass_converter.get_object(data=i, class_=BotCommand)
            for i in self._send_request(
                method="getMyCommands",
                parameters={
                    "scope": scope,
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            )
        ]

    def set_my_name(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        name: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyName",
            parameters={
                "name": name,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_name(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        language_code: Optional[str] = None
    ) -> BotName:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getMyName",
                parameters={
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            ),
            class_=BotName
        )

    def set_my_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        description: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyDescription",
            parameters={
                "description": description,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        language_code: Optional[str] = None
    ) -> BotDescription:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getMyDescription",
                parameters={
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            ),
            class_=BotDescription
        )

    def set_my_short_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        short_description: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyShortDescription",
            parameters={
                "short_description": short_description,
                "language_code": language_code
            },
            timeout_secs=timeout_secs
        )

    def get_my_short_description(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        language_code: Optional[str] = None
    ) -> BotShortDescription:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getMyShortDescription",
                parameters={
                    "language_code": language_code
                },
                timeout_secs=timeout_secs
            ),
            class_=BotShortDescription
        )

    def set_chat_menu_button(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Optional[int] = None,
        menu_button: Optional[MenuButton] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setChatMenuButton",
            parameters={
                "chat_id": chat_id,
                "menu_button": menu_button
            },
            timeout_secs=timeout_secs
        )

    def get_chat_menu_button(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Optional[int] = None
    ) -> Literal[True]:
        return self._send_request(
            method="getChatMenuButton",
            parameters={
                "chat_id": chat_id
            },
            timeout_secs=timeout_secs
        )

    def set_my_default_administrator_rights(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        rights: Optional[ChatAdministratorRights] = None,
        for_channels: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setMyDefaultAdministratorRights",
            parameters={
                "rights": rights,
                "for_channels": for_channels
            },
            timeout_secs=timeout_secs
        )

    def get_my_default_administrator_rights(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        for_channels: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="getMyDefaultAdministratorRights",
            parameters={
                "for_channels": for_channels
            },
            timeout_secs=timeout_secs
        )

    def edit_message_text(
        self,
        text: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        entities: Optional[list[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageText",
            parameters={
                "text": text,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "parse_mode": self._get_parse_mode(parse_mode, with_entities=bool(entities)),
                "entities": entities,
                "link_preview_options": link_preview_options,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def edit_message_caption(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Union[str, None, NotSet] = NOT_SET,
        caption_entities: Optional[list[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageCaption",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "caption": caption,
                "parse_mode": self._get_parse_mode(
                    parse_mode,
                    with_entities=bool(caption_entities)
                ),
                "caption_entities": caption_entities,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def edit_message_media(
        self,
        media: InputMedia,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageMedia",
            parameters={
                "media": media,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def edit_message_reply_markup(
        self,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Union[int, str, None] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="editMessageReplyMarkup",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id,
                "reply_markup": reply_markup
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Poll:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="stopPoll",
                parameters={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Poll
        )

    def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMessage",
            parameters={
                "chat_id": chat_id,
                "message_id": message_id
            },
            timeout_secs=timeout_secs
        )

    def delete_messages(
        self,
        chat_id: Union[int, str],
        message_ids: list[int],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteMessages",
            parameters={
                "chat_id": chat_id,
                "message_ids": message_ids
            },
            timeout_secs=timeout_secs
        )

    def send_sticker(
        self,
        chat_id: Union[int, str],
        sticker: Union[InputFile, str],
        *,
        timeout_secs: Union[int, float, None] = None,
        emoji: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Union[InlineKeyboardMarkup,
                            ReplyKeyboardMarkup,
                            ReplyKeyboardRemove,
                            ForceReply,
                            None] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendSticker",
                parameters={
                    "chat_id": chat_id,
                    "sticker": sticker,
                    "emoji": emoji,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def get_sticker_set(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> StickerSet:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="getStickerSet",
                parameters={
                    "name": name
                },
                timeout_secs=timeout_secs
            ),
            class_=StickerSet
        )

    def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: list[str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> list[Sticker]:
        return [
            self._dataclass_converter.get_object(data=i, class_=Sticker)
            for i in self._send_request(
                method="getCustomEmojiStickers",
                parameters={
                    "custom_emoji_ids": custom_emoji_ids
                },
                timeout_secs=timeout_secs
            )
        ]

    def upload_sticker_file(
        self,
        user_id: int,
        sticker: InputFile,
        sticker_format: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> File:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="uploadStickerFile",
                parameters={
                    "user_id": user_id,
                    "sticker": sticker,
                    "sticker_format": sticker_format
                },
                timeout_secs=timeout_secs
            ),
            class_=File
        )

    def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: list[InputSticker],
        sticker_format: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        sticker_type: Optional[str] = None,
        needs_repainting: Optional[bool] = None
    ) -> Literal[True]:
        return self._send_request(
            method="createNewStickerSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "title": title,
                "stickers": stickers,
                "sticker_format": sticker_format,
                "sticker_type": sticker_type,
                "needs_repainting": needs_repainting
            },
            timeout_secs=timeout_secs
        )

    def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: InputSticker,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="addStickerToSet",
            parameters={
                "user_id": user_id,
                "name": name,
                "sticker": sticker
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerPositionInSet",
            parameters={
                "sticker": sticker,
                "position": position
            },
            timeout_secs=timeout_secs
        )

    def delete_sticker_from_set(
        self,
        sticker: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteStickerFromSet",
            parameters={
                "sticker": sticker
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: list[str],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerEmojiList",
            parameters={
                "sticker": sticker,
                "emoji_list": emoji_list
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_keywords(
        self,
        sticker: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        keywords: Optional[list[str]] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerKeywords",
            parameters={
                "sticker": sticker,
                "keywords": keywords
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_mask_position(
        self,
        sticker: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        mask_position: Optional[MaskPosition] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerMaskPosition",
            parameters={
                "sticker": sticker,
                "mask_position": mask_position
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_set_title(
        self,
        name: str,
        title: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerSetTitle",
            parameters={
                "name": name,
                "title": title
            },
            timeout_secs=timeout_secs
        )

    def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        custom_emoji_id: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setCustomEmojiStickerSetThumbnail",
            parameters={
                "name": name,
                "custom_emoji_id": custom_emoji_id
            },
            timeout_secs=timeout_secs
        )

    def delete_sticker_set(
        self,
        name: str,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="deleteStickerSet",
            parameters={
                "name": name
            },
            timeout_secs=timeout_secs
        )

    def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        thumbnail: Union[InputFile, str, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setStickerSetthumbnail",
            parameters={
                "name": name,
                "user_id": user_id,
                "thumbnail": thumbnail
            },
            timeout_secs=timeout_secs
        )

    def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        *,
        timeout_secs: Union[int, float, None] = None,
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        button: Optional[InlineQueryResultsButton] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerInlineQuery",
            parameters={
                "inline_query_id": inline_query_id,
                "results": results,
                "cache_time": cache_time,
                "is_personal": is_personal,
                "next_offset": next_offset,
                "button": button
            },
            timeout_secs=timeout_secs
        )

    def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: InlineQueryResult,
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> SentWebAppMessage:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="answerWebAppQuery",
                parameters={
                    "web_app_query_id": web_app_query_id,
                    "result": result
                },
                timeout_secs=timeout_secs
            ),
            class_=SentWebAppMessage
        )

    def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[list[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendInvoice",
                parameters={
                    "chat_id": chat_id,
                    "title": title,
                    "description": description,
                    "payload": payload,
                    "provider_token": provider_token,
                    "currency": currency,
                    "prices": prices,
                    "message_thread_id": message_thread_id,
                    "max_tip_amount": max_tip_amount,
                    "suggested_tip_amounts": suggested_tip_amounts,
                    "start_parameter": start_parameter,
                    "provider_data": provider_data,
                    "photo_url": photo_url,
                    "photo_size": photo_size,
                    "photo_width": photo_width,
                    "photo_height": photo_height,
                    "need_name": need_name,
                    "need_phone_number": need_phone_number,
                    "need_email": need_email,
                    "need_shipping_address": need_shipping_address,
                    "send_phone_number_to_provider": send_phone_number_to_provider,
                    "send_email_to_provider": send_email_to_provider,
                    "is_flexible": is_flexible,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        *,
        timeout_secs: Union[int, float, None] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[list[int]] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None
    ) -> str:
        return self._send_request(
            method="createInvoiceLink",
            parameters={
                "title": title,
                "description": description,
                "payload": payload,
                "provider_token": provider_token,
                "currency": currency,
                "prices": prices,
                "max_tip_amount": max_tip_amount,
                "suggested_tip_amounts": suggested_tip_amounts,
                "provider_data": provider_data,
                "photo_url": photo_url,
                "photo_size": photo_size,
                "photo_width": photo_width,
                "photo_height": photo_height,
                "need_name": need_name,
                "need_phone_number": need_phone_number,
                "need_email": need_email,
                "need_shipping_address": need_shipping_address,
                "send_phone_number_to_provider": send_phone_number_to_provider,
                "send_email_to_provider": send_email_to_provider,
                "is_flexible": is_flexible
            },
            timeout_secs=timeout_secs
        )

    def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        *,
        timeout_secs: Union[int, float, None] = None,
        shipping_options: Optional[list[ShippingOption]] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerShippingQuery",
            parameters={
                "shipping_query_id": shipping_query_id,
                "ok": ok,
                "shipping_options": shipping_options,
                "error_message": error_message
            },
            timeout_secs=timeout_secs
        )

    def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        *,
        timeout_secs: Union[int, float, None] = None,
        error_message: Optional[str] = None
    ) -> Literal[True]:
        return self._send_request(
            method="answerPreCheckoutQuery",
            parameters={
                "pre_checkout_query_id": pre_checkout_query_id,
                "ok": ok,
                "error_message": error_message
            },
            timeout_secs=timeout_secs
        )

    def set_passport_data_errors(
        self,
        user_id: int,
        errors: list[PassportElementError],
        *,
        timeout_secs: Union[int, float, None] = None
    ) -> Literal[True]:
        return self._send_request(
            method="setPassportDataErrors",
            parameters={
                "user_id": user_id,
                "errors": errors
            },
            timeout_secs=timeout_secs
        )

    def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        *,
        timeout_secs: Union[int, float, None] = None,
        message_thread_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Message:
        return self._dataclass_converter.get_object(
            data=self._send_request(
                method="sendGame",
                parameters={
                    "chat_id": chat_id,
                    "game_short_name": game_short_name,
                    "message_thread_id": message_thread_id,
                    "disable_notification": disable_notification,
                    "protect_content": protect_content,
                    "reply_parameters": reply_parameters,
                    "reply_markup": reply_markup
                },
                timeout_secs=timeout_secs
            ),
            class_=Message
        )

    def set_game_score(
        self,
        user_id: int,
        score: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None
    ) -> Union[Message, Literal[True]]:
        data = self._send_request(
            method="setGameScore",
            parameters={
                "user_id": user_id,
                "score": score,
                "force": force,
                "disable_edit_message": disable_edit_message,
                "chat_id": chat_id,
                "message_id": message_id,
                "inline_message_id": inline_message_id
            },
            timeout_secs=timeout_secs
        )

        return data if data is True else self._dataclass_converter.get_object(
            data=data,
            class_=Message
        )

    def get_game_high_scores(
        self,
        user_id: int,
        *,
        timeout_secs: Union[int, float, None] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None
    ) -> list[GameHighScore]:
        return [
            self._dataclass_converter.get_object(data=i, class_=GameHighScore)
            for i in self._send_request(
                method="getGameHighScores",
                parameters={
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "inline_message_id": inline_message_id
                },
                timeout_secs=timeout_secs
            )
        ]

    def download_file(
        self,
        path: str,
        file: BinaryIO,
        *,
        timeout_secs: Union[int, float, None] = None,
        chunk_size: int = 64 * 1024
    ) -> None:
        if self.api_url == API_URL:
            with self.session.get(
                url=f"{API_URL}/file/bot{self.token}/{path}",
                stream=True,
                timeout=timeout_secs or self._timeout_secs
            ) as response:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
        else:
            with open(path, "rb") as local_file:
                while True:
                    chunk = local_file.read(chunk_size)

                    if not chunk:
                        break

                    file.write(chunk)

    def _send_request(
        self,
        method: str,
        *,
        parameters: Optional[dict[str, Any]] = None,
        timeout_secs: Union[int, float, None] = None
    ) -> Any:
        parameters = {
            name: value
            for name, value in (parameters or {}).items()
            if value is not None
        }

        if parameters:
            data, files = self._prepare_multipart_encoder(parameters)
            headers = {
                "Content-Type": data.content_type
            }
        else:
            data = headers = None
            files = []

        url = self._get_api_url(method)
        timeout_secs = timeout_secs or self._timeout_secs
        retries = 0

        while True:
            try:
                return self._process_response(
                    response=self.session.post(
                        url,
                        data=data,  # NOQA
                        headers=headers,
                        timeout=timeout_secs
                    ),
                    method=method,
                    parameters=parameters
                )
            except (RequestException, InternalServerError):
                if retries == self._retries:
                    raise

                retries += 1
                time.sleep(self._retry_delay_secs)
            except RetryAfterError as error:
                if not self._wait_on_rate_limit:
                    raise

                retries = 0
                time.sleep(error.retry_after)

            for i in files:
                i.seek(0)

    def _get_api_url(self, method: str) -> str:
        return f"{self.api_url}/bot{self.token}/{method}"

    def _get_parse_mode(
        self,
        parse_mode: Union[str, None, NotSet],
        *,
        with_entities: bool
    ) -> Optional[str]:
        if parse_mode is not NOT_SET:
            return parse_mode
        elif self._parse_mode is not NOT_SET and not with_entities:
            return self._parse_mode

    def _prepare_multipart_encoder(
        self,
        parameters: dict[str, Any]
    ) -> tuple[MultipartEncoder, list[IO]]:
        fields: dict[str, Any] = {}
        files: list[IO] = []

        for name, value in parameters.items():
            value = self._prepare_parameter_value(
                value,
                multipart_fields=fields,
                files=files,
                attach_files=False
            )

            if isinstance(value, (dict, list)):
                value = get_serialized_data(value)
            elif not isinstance(value, (str, tuple)):
                value = str(value)

            fields[name] = value

        return MultipartEncoder(fields), files

    def _prepare_parameter_value(
        self,
        value: Any,
        multipart_fields: dict[str, Any],
        files: list[IO],
        attach_files: bool = True,
    ) -> Any:
        if isinstance(value, InputFile):
            files.append(value.file)

            if attach_files:
                while True:
                    name = secrets.token_urlsafe(10)

                    if name not in multipart_fields:
                        break

                multipart_fields[name] = (value.name, value.file)

                return f"attach://{name}"

            return value.name, value.file
        elif is_dataclass(value):
            return {
                name: self._prepare_parameter_value(
                    value_,
                    multipart_fields=multipart_fields,
                    files=files
                )
                for name, value_ in self._dataclass_converter.get_data(value).items()
            }
        elif isinstance(value, datetime):
            return get_timestamp(value)
        elif isinstance(value, list):
            return [
                self._prepare_parameter_value(
                    i,
                    multipart_fields=multipart_fields,
                    files=files
                )
                for i in value
            ]

        return value

    def _process_response(
        self,
        response: Response,
        method: str,
        parameters: dict[str, Any]
    ) -> Any:
        data = response.json()

        if not data["ok"] or (response.status_code != HTTPStatus.OK):
            try:
                response_parameter_data = data["parameters"]
            except KeyError:
                response_parameters = None
            else:
                response_parameters = self._dataclass_converter.get_object(
                    data=response_parameter_data,
                    class_=ResponseParameters
                )

            raise get_request_error(
                method=method,
                parameters=parameters,
                status_code=response.status_code,
                description=data["description"],
                response_parameters=response_parameters
            )

        return data["result"]


class BotContext:

    def __init__(
        self,
        token: str,
        *,
        get_me: bool = True,
        api_url: str = API_URL,
        parse_mode: Union[str, NotSet] = NOT_SET,
        timeout_secs: Union[int, float, None] = 300,
        retries: int = 0,
        retry_delay_secs: Union[int, float] = 0,
        wait_on_rate_limit: bool = False
    ):
        self._token = token
        self._get_me = get_me
        self._api_url = api_url
        self._parse_mode = parse_mode
        self._timeout_secs = timeout_secs
        self._retries = retries
        self._retry_delay_secs = retry_delay_secs
        self._wait_on_rate_limit = wait_on_rate_limit
        self._session: Optional[Session] = None

    def __enter__(self) -> Bot:
        self._session = Session()
        bot = Bot(
            self._session,
            token=self._token,
            api_url=self._api_url,
            parse_mode=self._parse_mode,
            timeout_secs=self._timeout_secs,
            retries=self._retries,
            retry_delay_secs=self._retry_delay_secs,
            wait_on_rate_limit=self._wait_on_rate_limit
        )

        if self._get_me:
            bot.get_me()

        return bot

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()


def get_bot(
    token: str,
    *,
    get_me: bool = True,
    api_url: str = API_URL,
    parse_mode: Union[str, NotSet] = NOT_SET,
    timeout_secs: Union[int, float, None] = 300,
    retries: int = 0,
    retry_delay_secs: Union[int, float] = 0,
    wait_on_rate_limit: bool = False
) -> BotContext:
    return BotContext(
        token,
        get_me=get_me,
        api_url=api_url,
        parse_mode=parse_mode,
        timeout_secs=timeout_secs,
        retries=retries,
        retry_delay_secs=retry_delay_secs,
        wait_on_rate_limit=wait_on_rate_limit
    )
