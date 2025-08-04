class script(object):
    START_TXT = """Hello {}.
I'm An Auto-filter Bot Which Can Provide Movies In Your Groups.
○ Add Me To Your Group
○ Promote Me As Admin To Let Me Get In Action."""


    HELP_TXT = """Hey {}
Currently Using A Free Server, So Please Don’t Overload Me..."""

    ABOUT_TXT = """<b>
○ Creator     : <a href="https://github.com/aktelegram1">MMW BOTZ</a>
○ Language    : Python 3
○ Database    : MongoDB
○ Bot Server  : KoYeb</b>"""

    SOURCE_TXT = """<b>NOTE:</b>
○ Filter Bot Is Not A Open Source Project"""

    MANUELFILTER_TXT = """Help: <b>Filters</b>

Filter allows users to set automated replies for specific keywords.

<b>NOTE:</b>
○ Bot must be admin.  
○ Only admins can add filters.  
○ Alert buttons have a 64-character limit.

<b>Commands and Usage:</b>
• /filter – <code>Add a filter</code>  
• /filters – <code>List all filters</code>  
• /del – <code>Delete a filter</code>  
• /delall – <code>Delete all filters (owner only)</code>"""

    BUTTON_TXT = """Help: <b>Buttons</b>

Supports URL and alert inline buttons.

<b>NOTE:</b>
○ Message content is mandatory  
○ Works with any Telegram media  
○ Use Markdown formatting properly

<b>URL button format:</b>  
<code>[Button Text](buttonurl:https://github.com/mn-bots/ShobanaFilterBot)</code>

<b>Alert button format:</b>  
<code>[Button Text](buttonalert:This is an alert message)</code>"""

    AUTOFILTER_TXT = """<b>Note: File Indexing</b>

○ Make me admin in your channel (if private).  
○ Channel must not contain camrips, porn, or fake files.  
○ Forward last message to me with quote — I'll index those files.

<b>Note: AutoFilter</b>

○ Add me as admin in your group.  
○ Use /connect to link your group.  
○ Use /settings in PM to enable AutoFilter."""

    CONNECTION_TXT = """Help: <b>Connections</b>

Allows managing filters from PM, avoiding group spam.

<b>NOTE:</b>
○ Only admins can connect.  
○ Use <code>/connect</code> in group.

<b>Commands:</b>
• /connect – <code>Link group to PM</code>  
• /disconnect – <code>Unlink a chat</code>  
• /connections – <code>Show all connections</code>"""

    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>Commands:</b>
• /id – <code>Get user ID</code>  
• /info – <code>Get user info</code>  
• /imdb – <code>Fetch IMDb info</code>  
• /search – <code>Search movie from sources</code>  
• /start – <code>Bot status</code>  
• /ping – <code>Ping check</code>  
• /usage – <code>Bot usage</code>  
• /broadcast – <code>Broadcast (owner only)</code>"""

    ADMIN_TXT = """Help: <b>Admin Mods</b>

<b>NOTE:</b> Only bot admins can use these.

<b>Commands:</b>
• /logs – <code>Recent errors</code>  
• /stats – <code>File stats</code>  
• /delete – <code>Delete file</code>  
• /users – <code>User list</code>  
• /chats – <code>Chat list</code>  
• /leave – <code>Leave chat</code>  
• /disable – <code>Disable chat</code>  
• /ban – <code>Ban user</code>  
• /unban – <code>Unban user</code>  
• /channel – <code>Connected channels</code>  
• /broadcast – <code>Broadcast message</code>"""

    STATUS_TXT = """★ TOTAL FILES: <code>{}</code>
TOTAL USERS: <code>{}</code>
TOTAL CHATS: <code>{}</code>
USED STORAGE: <code>{}</code>
FREE STORAGE: <code>{}</code>"""

    LOG_TEXT_G = """#NewGroup
Group = {} (<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}"""

    RESULT_TXT = """<blockquote>Hey,</blockquote>
<blockquote>Just see what I found for your query.</blockquote>"""

    CUSTOM_FILE_CAPTION = """📂 Filename : {file_name}
FileSize : {file_size}

⚠️ <b>This file will be deleted within 1 minute due to copyright.</b>

<b>കോപ്പിറൈറ്റ് ഉള്ളതുകൊണ്ട് ഫയൽ 1 മിനിറ്റിനുള്ളിൽ ഇവിടെനിന്നും ഡിലീറ്റ് ആകുന്നതാണ്. അതിനാൽ, ഫയൽ ഡൗൺലോഡ് ചെയ്യുന്നതിന് മുമ്പ് മറ്റൊരു സ്ഥലത്തേക്ക് മാറ്റുക.</b>"""

    RESTART_GC_TXT = """<b>Bot Restarted!</b>

📅 Date: <code>{}</code>  
⏰ Time: <code>{}</code>  
🌐 Timezone: <code>Asia/Kolkata</code>  
🛠️ Build: <code>v1 [Stable]</code>"""

    LOG_TEXT_P = """#NewUser  
ID - <code>{}</code>  
Name - {}"""

    SPOLL_NOT_FND = """
I couldn't find anything related to your request. Try following the tips below:

<blockquote>
1️ Ask in correct spelling  
2️ Don’t request unreleased movies  
3️ Try format: [movie name language] or [movie year]
</blockquote>

<b>This movie is not added to the database yet.</b>
<pre>Report to admin using /bugs</pre>"""

    ENG_SPELL = """Please Note:  
1️⃣ Ask in correct spelling  
2️⃣ Don’t ask for unreleased movies  
3️⃣ Use format: [movie name language] or [movie year]"""

    MAL_SPELL = """ദയവായി ശ്രദ്ധിക്കുക:  
1️⃣ ശരിയായ അക്ഷരവിന്യാസം  
2️⃣ റിലീസ് ചെയ്യാത്ത സിനിമകൾ ചോദിക്കരുത്  
3️⃣ [പേര് ഭാഷ] അല്ലെങ്കിൽ [വർഷം] പോലെ ചോദിക്കുക"""

    HIN_SPELL = """कृपया ध्यान दें:  
1️⃣ सही वर्तनी  
2️⃣ रिलीज़ न हुई फ़िल्में न पूछें  
3️⃣ [नाम भाषा] या [साल] जैसे पूछें"""

    TAM_SPELL = """குறிப்பு:  
1️⃣ சரியான எழுத்துப்பிழை  
2️⃣ வெளியான படங்களைக் கேளுங்கள்  
3️⃣ [பட பெயர், ஆண்டு] போல கேளுங்கள்"""

    CHK_MOV_ALRT = """Checking file in my database..."""

    OLD_MES = """You're using an old message. Please resend the request."""

    MOV_NT_FND = """<b>This movie is not yet released or added to the database.</b>  
<pre>Report to admin using /bugs</pre>"""

    RESTART_TXT = """<b><u>Bot Restarted ✅</u></b>"""
