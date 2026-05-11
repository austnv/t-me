from fastapi import FastAPI, Request, Query
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
from typing import Optional
import re


app = FastAPI(title='t.uvpn.shop')


app.mount("/img", StaticFiles(directory="img"), name="img")


@app.get("/contact/{token}")
async def temporary_profile_links(token: str):
    """[Temporary profile links](https://core.telegram.org/api/links#temporary-profile-links)"""
    return RedirectResponse(f"tg://contact?token={quote(token)}")


@app.get("/+{phone_number}")
async def phone_number_links(
    phone_number: str,
    text: Optional[str] = None,
    profile: Optional[str] = None
):
    """[Phone number links](https://core.telegram.org/api/links#phone-number-links)"""
    params = [f"phone={quote(phone_number)}"]
    if text:
        params.append(f"text={quote(text)}")
    if profile is not None:
        params.append("profile")
    return RedirectResponse(f"tg://resolve?{'&'.join(params)}")


@app.get("/joinchat/{hash}")
async def chat_invite_links_legacy(hash: str):
    """[Chat invite links (legacy)](https://core.telegram.org/api/links#chat-invite-links)"""
    return RedirectResponse(f"tg://join?invite={quote(hash)}")


@app.get("/+{hash:path}")
async def chat_invite_links(hash: str):
    """[Chat invite links](https://core.telegram.org/api/links#chat-invite-links)"""
    return RedirectResponse(f"tg://join?invite={quote(hash.lstrip('/'))}")


@app.get("/addlist/{slug}")
async def chat_folder_links(slug: str):
    """[Chat folder links](https://core.telegram.org/api/links#chat-folder-links)"""
    return RedirectResponse(f"tg://addlist?slug={quote(slug)}")


@app.get("/c/{channel}/{id}")
async def message_links_private(
    channel: str,
    id: str,
    single: Optional[str] = None,
    thread: Optional[str] = None,
    comment: Optional[str] = None,
    t: Optional[str] = None
):
    """[Message links (private)](https://core.telegram.org/api/links#message-links)"""
    params = [f"channel={quote(channel)}", f"post={quote(id)}"]
    if single is not None:
        params.append("single")
    if thread:
        params.append(f"thread={quote(thread)}")
    if comment:
        params.append(f"comment={quote(comment)}")
    if t:
        params.append(f"t={quote(t)}")
    return RedirectResponse(f"tg://privatepost?{'&'.join(params)}")


@app.get("/c/{channel}/{thread_id}/{id}")
async def message_links_private_thread(
    channel: str,
    thread_id: str,
    id: str,
    single: Optional[str] = None,
    comment: Optional[str] = None,
    t: Optional[str] = None
):
    """[Message links (private with thread)](https://core.telegram.org/api/links#message-links)"""
    params = [f"channel={quote(channel)}", f"post={quote(id)}", f"thread={quote(thread_id)}"]
    if single is not None:
        params.append("single")
    if comment:
        params.append(f"comment={quote(comment)}")
    if t:
        params.append(f"t={quote(t)}")
    return RedirectResponse(f"tg://privatepost?{'&'.join(params)}")


@app.get("/share")
@app.get("/share/url")
@app.get("/share/url/")
async def share_links(
    url: str,
    text: Optional[str] = None
):
    """[Share links](https://core.telegram.org/api/links#share-links)"""
    params = [f"url={quote(url)}"]
    if text:
        params.append(f"text={quote(text)}")
    return RedirectResponse(f"tg://msg_url?{'&'.join(params)}")


@app.get("/m/{slug}")
async def business_chat_links(slug: str):
    """[Business chat links](https://core.telegram.org/api/links#business-chat-links)"""
    return RedirectResponse(f"tg://message?slug={quote(slug)}")


@app.get("/call/{slug}")
async def conference_links(slug: str):
    """[Conference links](https://core.telegram.org/api/links#conference-links)"""
    return RedirectResponse(f"tg://call?slug={quote(slug)}")


@app.get("/addstickers/{slug}")
async def stickerset_links(slug: str):
    """[Stickerset links](https://core.telegram.org/api/links#stickerset-links)"""
    return RedirectResponse(f"tg://addstickers?set={quote(slug)}")


@app.get("/addemoji/{slug}")
async def custom_emoji_stickerset_links(slug: str):
    """[Custom emoji stickerset links](https://core.telegram.org/api/links#custom-emoji-stickerset-links)"""
    return RedirectResponse(f"tg://addemoji?set={quote(slug)}")


@app.get("/boost/{username}")
async def boost_links_public(username: str):
    """Boost links (public channels)"""
    return RedirectResponse(f"tg://boost?domain={quote(username)}")


@app.get("/boost")
async def boost_links_private(c: str):
    """Boost links (private channels)"""
    return RedirectResponse(f"tg://boost?channel={quote(c)}")


@app.get("/proxy")
async def mtproxy_links(
    server: str,
    port: str,
    secret: str
):
    """MTProxy links"""
    params = [f"server={quote(server)}", f"port={quote(port)}", f"secret={quote(secret)}"]
    return RedirectResponse(f"tg://proxy?{'&'.join(params)}")


@app.get("/socks")
async def socks5_proxy_links(
    server: str,
    port: str,
    user: Optional[str] = None,
    pass_: Optional[str] = Query(None, alias="pass")
):
    """Socks5 proxy links"""
    params = [f"server={quote(server)}", f"port={quote(port)}"]
    if user:
        params.append(f"user={quote(user)}")
    if pass_:
        params.append(f"pass={quote(pass_)}")
    return RedirectResponse(f"tg://socks?{'&'.join(params)}")


@app.get("/addtheme/{name}")
async def theme_links(name: str):
    """Theme links"""
    return RedirectResponse(f"tg://addtheme?slug={quote(name)}")


@app.get("/bg/{hex_color}")
async def wallpaper_links_solid_fill(hex_color: str):
    """Wallpaper links (solid fill) - /bg/<hex_color>"""
    if re.match(r'^[0-9a-fA-F]{6}$', hex_color):
        return RedirectResponse(f"tg://bg?color={quote(hex_color)}")


@app.get("/bg/{top_color}-{bottom_color}")
async def wallpaper_links_gradient_fill(
    top_color: str,
    bottom_color: str,
    rotation: Optional[str] = None
):
    """Wallpaper links (gradient fill)"""
    params = [f"gradient={quote(top_color)}-{quote(bottom_color)}"]
    if rotation:
        params.append(f"rotation={quote(rotation)}")
    return RedirectResponse(f"tg://bg?{'&'.join(params)}")


@app.get("/bg/{slug:path}")
async def wallpaper_links_image(
    request: Request,
    slug: str,
    mode: Optional[str] = None,
    intensity: Optional[str] = None,
    bg_color: Optional[str] = None,
    rotation: Optional[str] = None
):
    """Wallpaper links (image, solid pattern, gradient pattern)"""
    slug = slug.lstrip('/')
    
    # Проверяем на freeform градиент
    if '~' in slug:
        return RedirectResponse(f"tg://bg?gradient={quote(slug)}")
    
    params = [f"slug={quote(slug)}"]
    if intensity:
        params.append(f"intensity={quote(intensity)}")
    if bg_color:
        params.append(f"bg_color={quote(bg_color)}")
    if rotation:
        params.append(f"rotation={quote(rotation)}")
    if mode:
        params.append(f"mode={quote(mode)}")
    return RedirectResponse(f"tg://bg?{'&'.join(params)}")


@app.get("/login/{code}")
async def login_code_link(code: str):
    """Login code link"""
    return RedirectResponse(f"tg://login?code={quote(code)}")


@app.get("/invoice/{slug}")
async def invoice_links(slug: str):
    """Invoice links"""
    return RedirectResponse(f"tg://invoice?slug={quote(slug)}")


@app.get("/$/{slug}")
async def invoice_links_alt(slug: str):
    """Invoice links (alt syntax /$/)"""
    return RedirectResponse(f"tg://invoice?slug={quote(slug)}")


@app.get("/setlanguage/{slug}")
async def language_pack_links(slug: str):
    """Language pack links"""
    return RedirectResponse(f"tg://setlanguage?lang={quote(slug)}")


@app.get("/confirmphone")
async def phone_confirmation_links(
    phone: str,
    hash: str
):
    """Phone confirmation links"""
    return RedirectResponse(f"tg://confirmphone?phone={quote(phone)}&hash={quote(hash)}")


@app.get("/giftcode/{slug}")
async def premium_giftcode_links(slug: str):
    """Premium giftcode links"""
    return RedirectResponse(f"tg://giftcode?slug={quote(slug)}")


@app.get("/nft/{slug}")
async def collectible_gift_link(slug: str):
    """Collectible gift link"""
    return RedirectResponse(f"tg://nft?slug={quote(slug)}")


@app.get("/{username}/s/{story_id}")
async def story_links(username: str, story_id: str):
    """Story links"""
    return RedirectResponse(f"tg://resolve?domain={quote(username)}&story={quote(story_id)}")


@app.get("/{username}/a/{album_id}")
async def story_album_links(username: str, album_id: str):
    """Story album links"""
    return RedirectResponse(f"tg://resolve?domain={quote(username)}&album={quote(album_id)}")


@app.get("/{username}/c/{collection_id}")
async def gift_collection_links(username: str, collection_id: str):
    """Gift collection links"""
    return RedirectResponse(f"tg://resolve?domain={quote(username)}&collection={quote(collection_id)}")


@app.get("/{username}/{id}")
async def message_links_public(
    username: str,
    id: str,
    single: Optional[str] = None,
    thread: Optional[str] = None,
    comment: Optional[str] = None,
    t: Optional[str] = None
):
    """Message links (public)"""
    params = [f"domain={quote(username)}", f"post={quote(id)}"]
    if single is not None:
        params.append("single")
    if thread:
        params.append(f"thread={quote(thread)}")
    if comment:
        params.append(f"comment={quote(comment)}")
    if t:
        params.append(f"t={quote(t)}")
    return RedirectResponse(f"tg://resolve?{'&'.join(params)}")


@app.get("/{username}/{thread_id}/{id}")
async def message_links_public_thread(
    username: str,
    thread_id: str,
    id: str,
    single: Optional[str] = None,
    comment: Optional[str] = None,
    t: Optional[str] = None
):
    """Message links (public with thread)"""
    params = [f"domain={quote(username)}", f"post={quote(id)}", f"thread={quote(thread_id)}"]
    if single is not None:
        params.append("single")
    if comment:
        params.append(f"comment={quote(comment)}")
    if t:
        params.append(f"t={quote(t)}")
    return RedirectResponse(f"tg://resolve?{'&'.join(params)}")


@app.get("/{bot_username}/{short_name}")
async def direct_mini_app_links(
    bot_username: str,
    short_name: str,
    startapp: Optional[str] = None,
    mode: Optional[str] = None
):
    """Direct mini app links"""
    params = [f"domain={quote(bot_username)}", f"appname={quote(short_name)}"]
    if startapp:
        params.append(f"startapp={quote(startapp)}")
    if mode:
        params.append(f"mode={quote(mode)}")
    return RedirectResponse(f"tg://resolve?{'&'.join(params)}")


# Общий обработчик для всех username ссылок
@app.get("/{username:path}")
async def public_username_links(
    request: Request,
    username: str
):
    """Public username links + все параметры"""
    username = username.rstrip('/')
    params = dict(request.query_params)
    
    # Собираем tg://resolve
    resolve_params = [f"domain={quote(username)}"]
    
    # Обрабатываем все возможные параметры
    if 'profile' in params:
        resolve_params.append("profile")
    
    if 'direct' in params:
        resolve_params.append("direct")
    
    if 'start' in params and params['start']:
        resolve_params.append(f"start={quote(params['start'])}")
    elif 'start' in params:
        pass  # start без значения не добавляем
    
    if 'startgroup' in params:
        if params['startgroup']:
            resolve_params.append(f"startgroup={quote(params['startgroup'])}")
        else:
            resolve_params.append("startgroup")
    
    if 'startchannel' in params:
        resolve_params.append("startchannel")
    
    if 'game' in params and params['game']:
        resolve_params.append(f"game={quote(params['game'])}")
    
    if 'videochat' in params:
        if params['videochat']:
            resolve_params.append(f"videochat={quote(params['videochat'])}")
        else:
            resolve_params.append("videochat")
    
    if 'livestream' in params:
        if params['livestream']:
            resolve_params.append(f"livestream={quote(params['livestream'])}")
        else:
            resolve_params.append("livestream")
    
    if 'voicechat' in params:
        if params['voicechat']:
            resolve_params.append(f"voicechat={quote(params['voicechat'])}")
        else:
            resolve_params.append("voicechat")
    
    if 'boost' in params:
        resolve_params.append("boost")
    
    if 'startapp' in params:
        if params['startapp']:
            resolve_params.append(f"startapp={quote(params['startapp'])}")
        else:
            resolve_params.append("startapp")
    
    if 'startattach' in params:
        if params['startattach']:
            resolve_params.append(f"startattach={quote(params['startattach'])}")
        else:
            resolve_params.append("startattach")
    
    if 'attach' in params and params['attach']:
        resolve_params.append(f"attach={quote(params['attach'])}")
    
    if 'album' in params and params['album']:
        resolve_params.append(f"album={quote(params['album'])}")
    
    if 'collection' in params and params['collection']:
        resolve_params.append(f"collection={quote(params['collection'])}")
    
    if 'ref' in params and params['ref']:
        resolve_params.append(f"ref={quote(params['ref'])}")
    
    if 'text' in params and params['text']:
        resolve_params.append(f"text={quote(params['text'])}")
    
    if 'mode' in params and params['mode']:
        resolve_params.append(f"mode={quote(params['mode'])}")
    
    if 'admin' in params and params['admin']:
        resolve_params.append(f"admin={quote(params['admin'])}")
    
    if 'choose' in params and params['choose']:
        resolve_params.append(f"choose={quote(params['choose'])}")
    
    if 'single' in params:
        resolve_params.append("single")
    
    if 'thread' in params and params['thread']:
        resolve_params.append(f"thread={quote(params['thread'])}")
    
    if 'comment' in params and params['comment']:
        resolve_params.append(f"comment={quote(params['comment'])}")
    
    if 't' in params and params['t']:
        resolve_params.append(f"t={quote(params['t'])}")
    
    if 'story' in params and params['story']:
        resolve_params.append(f"story={quote(params['story'])}")
    
    if not username:
        return FileResponse('index.html')

    return RedirectResponse(f"tg://resolve?{'&'.join(resolve_params)}")