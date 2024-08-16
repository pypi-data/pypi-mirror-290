import aiohttp
import asyncio
import logging
import json
import tgram
import os
import io
import ssl
import certifi
import inspect

from .methods import TelegramBotMethods
from .decorators import Decorators
from .errors import APIException
from .utils import API_URL, get_file_name, ALL_UPDATES
from .sync import wrap
from .types.type_ import Type_
from concurrent.futures.thread import ThreadPoolExecutor

from typing import List, Any, Literal, Callable, Union

from pathlib import Path
from importlib import import_module

from aiohttp.hdrs import USER_AGENT
from aiohttp.http import SERVER_SOFTWARE

logger = logging.getLogger(__name__)


class Dispatcher:
    async def run_for_updates(self: "TgBot", skip_updates: bool = None) -> None:
        if self.plugins:
            self.load_plugins()
        offset, allowed_updates, limit = (
            -1
            if (self.skip_updates if skip_updates is None else skip_updates)
            else None,
            self.allowed_updates,
            100,
        )
        self.is_running = True
        self.me = await self.get_me()

        while self.is_running:
            try:
                updates = await self.get_updates(
                    offset=offset,
                    limit=limit,
                    allowed_updates=allowed_updates,
                    timeout=55,
                )
                for update in updates:
                    offset = update.update_id + 1
                    await self._check_update(update)
            except (asyncio.CancelledError, KeyboardInterrupt):
                self.is_running = False
            except tgram.StopPropagation:
                pass
            except Exception as e:
                logger.exception(e)

        session = await self._get_session()
        await session.close()

    async def _check_cancel(self: "TgBot", callback: Callable, update: Any) -> bool:
        logger.debug("Checking listener in %s func", callback.__name__)
        try:
            if asyncio.iscoroutinefunction(callback):
                return await callback(self, update)
            else:
                return await self.loop.run_in_executor(
                    self.executor, callback, self, update
                )
        except Exception as e:
            logger.exception(e)

    async def _check_update(self: "TgBot", update: "tgram.types.Update") -> None:
        for listener in self._listen_handlers:
            if (attr := getattr(update, listener.update_type)) and listener.filters(
                attr
            ):
                self._listen_handlers.remove(listener)
                if listener.cancel is not None:
                    result = await self._check_cancel(listener.cancel, attr)
                    if result:
                        return
                return await self._process_listener(
                    attr, listener.next_step, listener.data
                )

        for handler in self._handlers:
            if handler.type == "all":
                await self._process_update(update, handler.callback)
            elif (attr := getattr(update, handler.type)) and handler.filter(attr):
                await self._process_update(attr, handler.callback)

    async def _process_listener(
        self: "TgBot", update: Any, callback: Callable, data: dict
    ) -> None:
        logger.debug("Processing listener to %s func", callback.__name__)
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(self, update, data)
            else:
                await self.loop.run_in_executor(
                    self.executor, callback, self, update, data
                )
        except Exception as e:
            logger.exception(e)

    async def _process_update(self: "TgBot", update: Any, callback: Callable) -> None:
        logger.debug("Processing update to %s func", callback.__name__)
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(self, update)
            else:
                await self.loop.run_in_executor(self.executor, callback, self, update)
        except Exception as e:
            logger.exception(e)


class TgBot(TelegramBotMethods, Decorators, Dispatcher):
    def __init__(
        self,
        bot_token: str,
        api_url: str = API_URL,
        allowed_updates: List[str] = [],
        link_preview_options: tgram.types.LinkPreviewOptions = None,
        parse_mode: Literal["Markdown", "MarkdownV2", "HTML"] = None,
        protect_content: bool = None,
        workers: int = None,
        retry_after: Union[int, bool] = None,
        plugins: Union[Path, str] = None,
        skip_updates: bool = True,
    ) -> None:
        self.bot_token = bot_token
        self.api_url = api_url
        self.allowed_updates = allowed_updates
        self.link_preview_options = link_preview_options
        self.parse_mode = parse_mode
        self.protect_content = protect_content
        self.workers = workers or min(32, (os.cpu_count() or 0) + 4)
        self.retry_after = retry_after
        self.plugins = Path(plugins) if isinstance(plugins, str) else plugins
        self.skip_updates = skip_updates
        self.executor = ThreadPoolExecutor(self.workers, thread_name_prefix="Handlers")
        self.loop = asyncio.get_event_loop()

        self.is_running: bool = None
        self.me: "tgram.types.User" = None

        self._listen_handlers: List["tgram.types.Listener"] = []
        self._handlers: List["tgram.handlers.Handler"] = []
        self._custom_types: dict = {}
        self._session: "aiohttp.ClientSession" = None

        if not api_url.endswith("/"):
            api_url += "/"

        self._api_url: str = f"{api_url}bot{bot_token}/"

    def add_handler(self, handler: "tgram.handlers.Handler") -> None:
        if handler.type == "all":
            self.allowed_updates = ALL_UPDATES
        elif handler.type not in self.allowed_updates:
            self.allowed_updates.append(handler.type)

        logger.info(
            "(%s) added to %s handlers",
            handler.callback.__name__,
            "Update." + handler.type if handler.type != "all" else "all",
        )
        self._handlers.append(handler)

    async def _new_session(self) -> None:
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=100,
                ssl_context=ssl.create_default_context(cafile=certifi.where()),
                ttl_dns_cache=3600,
            ),
            headers={USER_AGENT: f"{SERVER_SOFTWARE} tgram/{tgram.__version__}"},
        )
        self._session = session

    async def _get_session(self) -> "aiohttp.ClientSession":
        if self._session is None or self._session.closed:
            await self._new_session()
        elif not self._session.loop.is_running():
            await self._session.close()
            await self._new_session()

        return self._session

    async def _send_request(self, method: str, **kwargs) -> Any:
        request_url = self._api_url + method
        if method != "getUpdates":
            logger.info("Sending request using the method: %s", method)
        session = await self._get_session()
        data = aiohttp.FormData(quote_fields=False)
        has_files, file = False, None

        for key, value in kwargs.items():
            if value is None or key == "timeout" or key == "retry":
                continue
            if isinstance(value, Path):
                has_files = True
                with open(value, "rb") as f:
                    value = f
                    file = f.read()
            elif isinstance(value, (io.BytesIO, io.BufferedReader, bytes)):
                has_files = True
                file = value if isinstance(value, bytes) else value.read()
            elif isinstance(value, (Type_, list)):
                value = json.dumps(value, ensure_ascii=False, default=Type_.default)
            else:
                value = str(value)
            data.add_field(
                key,
                file if has_files else value,
                filename=get_file_name(value) if has_files else None,
            )

        response = await session.request(
            "POST" if has_files else "GET",
            request_url,
            data=data,
            timeout=aiohttp.ClientTimeout(
                total=kwargs.get("timeout", 60 if not has_files else 300)
            ),
        )

        if not self.is_running:
            await session.close()

        response_json = await response.json()

        if not response_json["ok"]:
            if (
                response_json["error_code"] == 429
                and self.retry_after
                and (not kwargs.get("retry"))
            ):
                s = response_json["parameters"]["retry_after"]
                retry_after = (
                    s
                    if self.retry_after is True
                    else (s if s < self.retry_after else self.retry_after)
                )
                logger.warning(
                    "You got floodwait for %s seconds, I will retry after %s",
                    s,
                    retry_after,
                )
                await asyncio.sleep(retry_after)
                return await self._send_request(method, {"retry": 1, **kwargs})
            del response_json["ok"]
            raise APIException(json.dumps(response_json))

        return response_json

    def load_plugins(self) -> None:
        for path in sorted(self.plugins.rglob("*.py")):
            module_path = ".".join(path.parent.parts + (path.stem,))
            module = import_module(module_path)
            for name in vars(module).keys():
                obj = getattr(module, name)

                if hasattr(obj, "handlers"):
                    for handler in obj.handlers:
                        if isinstance(handler, tgram.handlers.Handler):
                            self.add_handler(handler)

    def customize(self, old: type, new: type) -> Literal[True]:
        if Type_ not in inspect.getmro(old):
            raise ValueError("You can't customize this type, it's not tgram type.")

        wrap(new)

        self._custom_types.update({old.__name__: new})

        return True


wrap(Dispatcher)
wrap(TelegramBotMethods)
