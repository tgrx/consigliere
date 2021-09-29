from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

from pydantic import Field

from .base import Str64
from .base import TelegramBotApiType
from .base import update_forward_refs


class User(TelegramBotApiType):
    """
    This object represents a Telegram user or bot.
    https://core.telegram.org/bots/api#user
    """

    # fmt: off
    id: int = Field(..., description="Unique identifier for this user or bot. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.")  # noqa: A003, VNE003
    is_bot: bool = Field(..., description="True, if this user is a bot")
    first_name: str = Field(..., description="User's or bot's first name")
    last_name: Optional[str] = Field(None, description="Optional. User's or bot's last name")
    username: Optional[str] = Field(None, description="Optional. User's or bot's username")
    # fmt: on


class Chat(TelegramBotApiType):
    """
    This object represents a chat.
    https://core.telegram.org/bots/api#chat
    """

    # fmt: off
    id: int = Field(..., description="Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.")  # noqa: A003, VNE003
    title: Optional[str] = Field(None, description="Optional. Title, for supergroups, channels and group chats")
    username: Optional[str] = Field(None, description="Optional. Username, for private chats, supergroups and channels if available")
    # fmt: on


class MessageEntity(TelegramBotApiType):
    """
    This object represents one special entity in a text message.
    For example, hashtags, usernames, URLs, etc.
    https://core.telegram.org/bots/api#messageentity
    """

    # fmt: off
    type: str = Field(..., description="Type of the entity. Can be “mention” (@username), “hashtag” (#hashtag), “cashtag” ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org), “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text), “italic” (italic text), “underline” (underlined text), “strikethrough” (strikethrough text), “code” (monowidth string), “pre” (monowidth block), “text_link” (for clickable text URLs), “text_mention” (for users without usernames)")  # noqa: A003, VNE003
    offset: int = Field(..., description="Offset in UTF-16 code units to the start of the entity")
    length: int = Field(..., description="Length of the entity in UTF-16 code units")
    url: Optional[str] = Field(None, description="Optional. For “text_link” only, url that will be opened after user taps on the text")
    user: Optional[User] = Field(None, description="Optional. For “text_mention” only, the mentioned user")
    language: Optional[str] = Field(None, description="Optional. For “pre” only, the programming language of the entity text")
    # fmt: on


@update_forward_refs
class Message(TelegramBotApiType):
    """
    This object represents a message.
    https://core.telegram.org/bots/api#message
    """

    # fmt: off
    message_id: int = Field(..., description="Unique message identifier inside this chat")
    from_: Optional[User] = Field(None)
    date: datetime = Field(...)
    chat: Chat = Field(...)
    edit_date: Optional[datetime] = Field(None)
    reply_to_message: Optional["Message"] = Field(None)
    text: Optional[str] = Field(None)
    entities: List[MessageEntity] = Field(default_factory=list)
    # fmt: on

    class Config:
        fields = {
            "from_": "from",
        }


class Update(TelegramBotApiType):
    """
    This object represents an incoming update.
    At most one of the optional parameters
        can be present in any given update.
    https://core.telegram.org/bots/api#update
    """

    # fmt: off
    update_id: int = Field(..., description="The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This ID becomes especially handy if you're using Webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially.")
    message: Optional[Message] = Field(None, description="Optional. New incoming message of any kind — text, photo, sticker, etc.")
    edited_message: Optional[Message] = Field(None, description="Optional. New version of a message that is known to the bot and was edited")
    channel_post: Optional[Message] = Field(None, description="Optional. New incoming channel post of any kind — text, photo, sticker, etc.")
    edited_channel_post: Optional[Message] = Field(None, description="Optional. New version of a channel post that is known to the bot and was edited")
    # fmt: on


class WebhookInfo(TelegramBotApiType):
    """
    Contains information about the current status of a webhook.
    https://core.telegram.org/bots/api#webhookinfo
    """

    # fmt: off
    url: str = Field(..., description="Webhook URL, may be empty if webhook is not set up")
    has_custom_certificate: bool = Field(..., description="True, if a custom certificate was provided for webhook certificate checks")
    pending_update_count: int = Field(0, description="Number of updates awaiting delivery")
    ip_address: Optional[str] = Field(None, description="Optional. Currently used webhook IP address")
    last_error_date: Optional[datetime] = Field(None, description="Optional. Unix time for the most recent error that happened when trying to deliver an update via webhook")
    last_error_message: Optional[str] = Field(None, description="Optional. Error message in human-readable format for the most recent error that happened when trying to deliver an update via webhook")
    max_connections: Optional[int] = Field(None, description="Optional. Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery")
    allowed_updates: List[str] = Field(default_factory=list, description="Optional. A list of update types the bot is subscribed to. Defaults to all update types except chat_member")
    # fmt: on


class InlineKeyboardButton(TelegramBotApiType):
    """
    This object represents one button of an inline keyboard.
    You MUST use exactly one of the optional fields.
    https://core.telegram.org/bots/api#inlinekeyboardbutton
    """

    # fmt: off
    text: str = Field(..., description="Label text on the button")
    url: Optional[str] = Field(None, description="Optional. HTTP or tg:// url to be opened when button is pressed")
    callback_data: Optional[Str64] = Field(None, description="Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes")
    # fmt: on


InlineKeyboardButtonRow = List[InlineKeyboardButton]


class InlineKeyboardMarkup(TelegramBotApiType):
    """
    This object represents an inline keyboard
        that appears right next to the message it belongs to.
    https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """

    # fmt: off
    inline_keyboard: List[InlineKeyboardButtonRow] = Field(default_factory=list, description="Array of button rows, each represented by an Array of InlineKeyboardButton objects")
    # fmt: on


class KeyboardButton(TelegramBotApiType):
    """
    This object represents one button of the reply keyboard.
    For simple text buttons String can be used
        instead of this object to specify text of the button.
    Optional fields request_contact, request_location,
        and request_poll are mutually exclusive.
    https://core.telegram.org/bots/api#keyboardbutton
    """

    # fmt: off
    text: str = Field(..., description="Text of the button. If none of the optional fields are used, it will be sent as a message when the button is pressed")
    # fmt: on


KeyboardButtonRow = List[KeyboardButton]


class ReplyKeyboardMarkup(TelegramBotApiType):
    """
    This object represents a custom keyboard with reply options
        (see Introduction to bots for details and examples).
        https://core.telegram.org/bots#keyboards
    https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    # fmt: off
    keyboard: List[KeyboardButtonRow] = Field(default_factory=list, description="Array of button rows, each represented by an Array of KeyboardButton objects")
    resize_keyboard: bool = Field(False, description="Optional. Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to false, in which case the custom keyboard is always of the same height as the app's standard keyboard.")
    one_time_keyboard: bool = Field(False, description="Optional. Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available, but clients will automatically display the usual letter-keyboard in the chat – the user can press a special button in the input field to see the custom keyboard again. Defaults to false.")
    # fmt: on


class ReplyKeyboardRemove(TelegramBotApiType):
    """
    Upon receiving a message with this object,
        Telegram clients will remove the current custom keyboard
        and display the default letter-keyboard.
    By default, custom keyboards are displayed
        until a new keyboard is sent by a bot.
    An exception is made for one-time keyboards
        that are hidden immediately
        after the user presses a button (see ReplyKeyboardMarkup).
    https://core.telegram.org/bots/api#replykeyboardremove
    """

    # fmt: off
    remove_keyboard: bool = Field(True, description="Requests clients to remove the custom keyboard (user will not be able to summon this keyboard; if you want to hide the keyboard from sight but keep it accessible, use one_time_keyboard in ReplyKeyboardMarkup)")
    # fmt: on


class ForceReply(TelegramBotApiType):
    """
    Upon receiving a message with this object,
        Telegram clients will display a reply interface to the user
        (act as if the user has selected the bot's message and tapped 'Reply').
    This can be extremely useful
        if you want to create user-friendly step-by-step interfaces
        without having to sacrifice privacy mode.

    Example: A poll bot for groups runs in privacy mode
        (only receives commands, replies to its messages and mentions).
    There could be two ways to create a new poll:

    -   Explain the user how to send a command with parameters
        (e.g. /newpoll question answer1 answer2).
        May be appealing for hardcore users but lacks modern day polish.
    -   Guide the user through a step-by-step process.
        'Please send me your question',
        'Cool, now let's add the first answer option',
        'Great. Keep adding answer options,
         then send /done when you're ready'.
        The last option is definitely more attractive.
        And if you use ForceReply in your bot's questions,
            it will receive the user's answers
            even if it only receives replies, commands and mentions —
            without any extra work for the user.

    https://core.telegram.org/bots/api#forcereply
    """

    # fmt: off
    force_reply: bool = Field(True, description="Shows reply interface to the user, as if they manually selected the bot's message and tapped 'Reply'")
    # fmt: on


ReplyMarkupType = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
]

__all__ = (
    Chat.__name__,
    ForceReply.__name__,
    InlineKeyboardButton.__name__,
    InlineKeyboardMarkup.__name__,
    KeyboardButton.__name__,
    Message.__name__,
    MessageEntity.__name__,
    ReplyKeyboardMarkup.__name__,
    ReplyKeyboardRemove.__name__,
    Update.__name__,
    User.__name__,
    WebhookInfo.__name__,
)
