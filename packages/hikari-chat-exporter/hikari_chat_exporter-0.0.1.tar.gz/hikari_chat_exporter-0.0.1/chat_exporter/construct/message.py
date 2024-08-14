import html
from typing import List, Optional, Union

from pytz import timezone
from datetime import timedelta

from chat_exporter.ext.discord_import import hikari

from chat_exporter.construct.assets import Attachment, Component, Embed, Reaction
from chat_exporter.ext.discord_utils import DiscordUtils
from chat_exporter.ext.html_generator import (
    fill_out,
    bot_tag,
    bot_tag_verified,
    message_body,
    message_pin,
    message_thread,
    message_content,
    message_reference,
    message_reference_unknown,
    message_interaction,
    img_attachment,
    start_message,
    end_message,
    PARSE_MODE_NONE,
    PARSE_MODE_MARKDOWN,
    PARSE_MODE_REFERENCE,
)


def _gather_user_bot(author: hikari.users.User):
    if author.is_bot and hikari.users.UserFlag.VERIFIED_BOT in author.flags:
        return bot_tag_verified
    elif author.is_bot:
        return bot_tag
    return ""


def _set_edit_at(message_edited_timestamp):
    return f'<span class="chatlog__reference-edited-timestamp" title="{message_edited_timestamp}">(edited)</span>'


class MessageConstruct:
    message_html: str = ""

    # Asset Types
    embeds: str = ""
    reactions: str = ""
    components: str = ""
    attachments: str = ""
    time_format: str = ""

    def __init__(
            self,
            message: hikari.messages.Message,
            previous_message: Optional[hikari.messages.Message],
            pytz_timezone,
            military_time: bool,
            guild: hikari.guilds.Guild,
            meta_data: dict
    ):
        self.message = message
        self.previous_message = previous_message
        self.pytz_timezone = pytz_timezone
        self.military_time = military_time
        self.guild = guild

        self.time_format = "%A, %e %B %Y %I:%M %p"
        if self.military_time:
            self.time_format = "%A, %e %B %Y %H:%M"

        self.message_created_at, self.message_edited_timestamp = self.set_time()
        self.meta_data = meta_data

    async def construct_message(
            self,
    ) -> (str, dict):
        if hikari.messages.MessageType.CHANNEL_PINNED_MESSAGE == self.message.type:
            await self.build_pin()
        else:
            await self.build_message()
        return self.message_html, self.meta_data

    async def build_message(self):
        await self.build_content()
        await self.build_reference()
        await self.build_interaction()
        await self.build_sticker()
        await self.build_assets()
        await self.build_message_template()
        await self.build_meta_data()

    async def build_pin(self):
        await self.generate_message_divider(channel_audit=True)
        await self.build_pin_template()

    async def build_thread(self):
        await self.generate_message_divider(channel_audit=True)
        await self.build_thread_template()

    async def build_meta_data(self):
        user_id = self.message.author.id

        if user_id in self.meta_data:
            self.meta_data[user_id][4] += 1
        else:
            user_name_discriminator = self.message.author.username + "#" + self.message.author.discriminator
            user_created_at = self.message.author.created_at
            user_bot = _gather_user_bot(self.message.author)
            user_avatar = (
                self.message.author.display_avatar_url if self.message.author.display_avatar_url
                else DiscordUtils.default_avatar
            )
            user_joined_at = self.message.author.joined_at if hasattr(self.message.author, "joined_at") else None
            user_display_name = (
                f'<div class="meta__display-name">{self.message.author.username}</div>'
                if self.message.author.username != self.message.author.username
                else ""
            )
            self.meta_data[user_id] = [
                user_name_discriminator, user_created_at, user_bot, user_avatar, 1, user_joined_at, user_display_name
            ]

    async def build_content(self):
        if not self.message.content:
            self.message.content = ""
            return

        if self.message_edited_timestamp:
            self.message_edited_timestamp = _set_edit_at(self.message_edited_timestamp)

        self.message.content = html.escape(self.message.content)
        self.message.content = await fill_out(self.guild, message_content, [
            ("MESSAGE_CONTENT", self.message.content, PARSE_MODE_MARKDOWN),
            ("EDIT", self.message_edited_timestamp, PARSE_MODE_NONE)
        ])

    async def build_reference(self):
        if not self.message.referenced_message:
            self.message.referenced_message = None
            return

        message = self.message.referenced_message

        guild_member = await self._gather_member(message.author)
        display_name = guild_member.display_name if guild_member else self.message.author.username

        is_bot = _gather_user_bot(message.author)
        user_colour = await self._gather_user_colour(message.author)

        if not message.content and not message.interaction:
            message.content = "Click to see attachment"
        elif not message.content and message.interaction:
            message.content = "Click to see command"

        icon = ""
        if not message.interaction and (message.embeds or message.attachments):
            icon = DiscordUtils.reference_attachment_icon
        elif message.interaction:
            icon = DiscordUtils.interaction_command_icon

        _, message_edited_timestamp = self.set_time(message)

        if message_edited_timestamp:
            message_edited_timestamp = _set_edit_at(message_edited_timestamp)

        avatar_url = message.author.display_avatar_url if message.author.display_avatar_url else DiscordUtils.default_avatar
        self.message.referenced_message = await fill_out(self.guild, message_reference, [
            ("AVATAR_URL", str(avatar_url), PARSE_MODE_NONE),
            ("BOT_TAG", is_bot, PARSE_MODE_NONE),
            ("NAME_TAG", "%s#%s" % (message.author.username, message.author.discriminator), PARSE_MODE_NONE),
            ("NAME", str(html.escape(display_name))),
            ("USER_COLOUR", user_colour, PARSE_MODE_NONE),
            ("CONTENT", message.content, PARSE_MODE_REFERENCE),
            ("EDIT", message_edited_timestamp, PARSE_MODE_NONE),
            ("ICON", icon, PARSE_MODE_NONE),
            ("USER_ID", str(message.author.id), PARSE_MODE_NONE),
            ("MESSAGE_ID", str(self.message.referenced_message.id), PARSE_MODE_NONE),
        ])

    async def build_interaction(self):
        if not self.message.interaction:
            self.message.interaction = ""
            return

        user: hikari.users.User = self.message.interaction.user
        is_bot = _gather_user_bot(user)
        user_colour = await self._gather_user_colour(user)
        avatar_url = user.display_avatar_url if user.display_avatar_url else DiscordUtils.default_avatar
        self.message.interaction = await fill_out(self.guild, message_interaction, [
            ("AVATAR_URL", str(avatar_url), PARSE_MODE_NONE),
            ("BOT_TAG", is_bot, PARSE_MODE_NONE),
            ("NAME_TAG", "%s#%s" % (user.global_name, user.discriminator), PARSE_MODE_NONE),
            ("NAME", str(html.escape(user.username))),
            ("USER_COLOUR", user_colour, PARSE_MODE_NONE),
            ("FILLER", "used ", PARSE_MODE_NONE),
            ("COMMAND", "/" + self.message.interaction.name, PARSE_MODE_NONE),
            ("USER_ID", str(user.id), PARSE_MODE_NONE),
            ("INTERACTION_ID", str(self.message.interaction.id), PARSE_MODE_NONE),
        ])

    async def build_sticker(self):
        if not self.message.stickers or not hasattr(self.message.stickers[0], "url"):
            return

        sticker_image_url = self.message.stickers[0].url

        if sticker_image_url.endswith(".json"):
            sticker = await self.message.stickers[0].fetch()
            sticker_image_url = (
                f"https://cdn.jsdelivr.net/gh/mahtoid/DiscordUtils@master/stickers/{sticker.pack_id}/{sticker.id}.gif"
            )

        self.message.content = await fill_out(self.guild, img_attachment, [
            ("ATTACH_URL", str(sticker_image_url), PARSE_MODE_NONE),
            ("ATTACH_URL_THUMB", str(sticker_image_url), PARSE_MODE_NONE)
        ])

    async def build_assets(self):
        for e in self.message.embeds:
            self.embeds += await Embed(e, self.guild).flow()

        for a in self.message.attachments:
            self.attachments += await Attachment(a, self.guild).flow()

        for c in self.message.components:
            self.components += await Component(c, self.guild).flow()

        for r in self.message.reactions:
            self.reactions += await Reaction(r, self.guild).flow()

        if self.reactions:
            self.reactions = f'<div class="chatlog__reactions">{self.reactions}</div>'

    async def build_message_template(self):
        started = await self.generate_message_divider()

        if started:
            return self.message_html

        self.message_html += await fill_out(self.guild, message_body, [
            ("MESSAGE_ID", str(self.message.id)),
            ("MESSAGE_CONTENT", self.message.content, PARSE_MODE_NONE),
            ("EMBEDS", self.embeds, PARSE_MODE_NONE),
            ("ATTACHMENTS", self.attachments, PARSE_MODE_NONE),
            ("COMPONENTS", self.components, PARSE_MODE_NONE),
            ("EMOJI", self.reactions, PARSE_MODE_NONE),
            ("TIMESTAMP", self.message_created_at, PARSE_MODE_NONE),
            ("TIME", self.message_created_at.split()[-1], PARSE_MODE_NONE),
        ])

        return self.message_html

    def _generate_message_divider_check(self):
        return bool(
            self.previous_message is None or self.message.referenced_message != "" or self.message.interaction != "" or
            self.previous_message.author.id != self.message.author.id or self.message.webhook_id is not None or
            self.message.created_at > (self.previous_message.created_at + timedelta(minutes=4))
        )

    async def generate_message_divider(self, channel_audit=False):
        if channel_audit or self._generate_message_divider_check():
            if self.previous_message is not None:
                self.message_html += await fill_out(self.guild, end_message, [])

            if channel_audit:
                return

            followup_symbol = ""
            is_bot = _gather_user_bot(self.message.author)

            guild_member = await self._gather_member(self.message.author)
            display_name = guild_member.display_name if guild_member else self.message.author.username

            avatar_url = self.message.author.avatar_url if self.message.author.avatar_url else DiscordUtils.default_avatar

            if self.message.referenced_message != "" or self.message.interaction:
                followup_symbol = "<div class='chatlog__followup-symbol'></div>"

            time = self.message.created_at
            if not self.message.created_at.tzinfo:
                time = timezone("UTC").localize(time)

            default_timestamp = time.astimezone(timezone(self.pytz_timezone)).strftime("%d-%m-%Y %H:%M")

            self.message_html += await fill_out(self.guild, start_message, [
                ("REFERENCE_SYMBOL", followup_symbol, PARSE_MODE_NONE),
                ("REFERENCE",
                 self.message.referenced_message if self.message.referenced_message else self.message.interaction,
                 PARSE_MODE_NONE),
                ("AVATAR_URL", str(avatar_url), PARSE_MODE_NONE),
                ("NAME_TAG", "%s#%s" % (self.message.author.username, self.message.author.discriminator),
                 PARSE_MODE_NONE),
                ("USER_ID", str(self.message.author.id)),
                ("USER_COLOUR", await self._gather_user_colour(self.message.author)),
                ("USER_ICON", await self._gather_user_icon(self.message.author), PARSE_MODE_NONE),
                ("NAME", str(html.escape(display_name))),
                ("BOT_TAG", str(is_bot), PARSE_MODE_NONE),
                ("TIMESTAMP", str(self.message_created_at)),
                ("DEFAULT_TIMESTAMP", str(default_timestamp), PARSE_MODE_NONE),
                ("MESSAGE_ID", str(self.message.id)),
                ("MESSAGE_CONTENT", self.message.content, PARSE_MODE_NONE),
                ("EMBEDS", self.embeds, PARSE_MODE_NONE),
                ("ATTACHMENTS", self.attachments, PARSE_MODE_NONE),
                ("COMPONENTS", self.components, PARSE_MODE_NONE),
                ("EMOJI", self.reactions, PARSE_MODE_NONE)
            ])

            return True

    async def build_pin_template(self):
        self.message_html += await fill_out(self.guild, message_pin, [
            ("PIN_URL", DiscordUtils.pinned_message_icon, PARSE_MODE_NONE),
            ("USER_COLOUR", await self._gather_user_colour(self.message.author)),
            ("NAME", str(html.escape(self.message.author.username))),
            ("NAME_TAG", "%s#%s" % (self.message.author.username, self.message.author.discriminator), PARSE_MODE_NONE),
            ("MESSAGE_ID", str(self.message.id), PARSE_MODE_NONE),
            ("REF_MESSAGE_ID", str(self.message.referenced_message.message_id), PARSE_MODE_NONE)
        ])

    async def build_thread_template(self):
        self.message_html += await fill_out(self.guild, message_thread, [
            ("THREAD_URL", DiscordUtils.thread_channel_icon,
             PARSE_MODE_NONE),
            ("THREAD_NAME", self.message.content, PARSE_MODE_NONE),
            ("USER_COLOUR", await self._gather_user_colour(self.message.author)),
            ("NAME", str(html.escape(self.message.author.username))),
            ("NAME_TAG", "%s#%s" % (self.message.author.username, self.message.author.discriminator), PARSE_MODE_NONE),
            ("MESSAGE_ID", str(self.message.id), PARSE_MODE_NONE),
        ])

    async def _gather_member(self, author: hikari.users.User):
        member = self.guild.get_member(author)

        if member:
            return member

        try:
            return await self.guild.fetch_member(author)
        except Exception:
            return None

    async def _gather_user_colour(self, author: hikari.users.User):
        member = await self._gather_member(author)
        user_colour = member.accent_colour if member and str(member.accent_colour) != "#000000" else "#FFFFFF"
        return f"color: {user_colour};"

    async def _gather_user_icon(self, author: hikari.users.User):
        member = await self._gather_member(author)

        if not member:
            return ""

        if hasattr(member, "display_icon") and member.display_icon:
            return f"<img class='chatlog__role-icon' src='{member.display_icon}' alt='Role Icon'>"
        elif hasattr(member, "top_role") and member.top_role and member.top_role.icon:
            return f"<img class='chatlog__role-icon' src='{member.top_role.icon}' alt='Role Icon'>"
        return ""

    def set_time(self, message: Optional[hikari.messages.Message] = None):
        message = message if message else self.message
        created_at_str = self.to_local_time_str(message.created_at)
        edited_at_str = self.to_local_time_str(message.edited_timestamp) if message.edited_timestamp else ""

        return created_at_str, edited_at_str

    def to_local_time_str(self, time):
        if not self.message.created_at.tzinfo:
            time = timezone("UTC").localize(time)

        local_time = time.astimezone(timezone(self.pytz_timezone))

        if self.military_time:
            return local_time.strftime(self.time_format)

        return local_time.strftime(self.time_format)


async def gather_messages(
        messages: List[hikari.messages.Message],
        guild: hikari.guilds.Guild,
        pytz_timezone,
        military_time,
) -> (str, dict):
    message_html: str = ""
    meta_data: dict = {}
    previous_message: Optional[hikari.messages.Message] = None

    for message in messages:
        content_html, meta_data = await MessageConstruct(
            message,
            previous_message,
            pytz_timezone,
            military_time,
            guild,
            meta_data
        ).construct_message()
        message_html += content_html
        previous_message = message

    message_html += "</div>"
    return message_html, meta_data
