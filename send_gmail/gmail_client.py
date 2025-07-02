#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmailクライアント

SMTPを使用してGmailでメールを送信するクライアントクラス
"""

import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from typing import Dict, List, Optional, Union, Any

from config import (
    EMAIL_USER, EMAIL_PASS, EMAIL_FROM,
    SMTP_SERVER, SMTP_PORT,
    MAX_RETRIES, RETRY_DELAY, BACKOFF_FACTOR, DEBUG
)

# ロガーの設定
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GmailClient:
    """
    Gmailクライアントクラス
    
    SMTPを使用してGmailでメールを送信するクライアントクラス
    エラー時の再送信機能を実装
    """
    
    def __init__(
        self, 
        user: Optional[str] = None, 
        password: Optional[str] = None,
        from_email: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
        retry_delay: int = RETRY_DELAY,
        backoff_factor: int = BACKOFF_FACTOR
    ):
        """
        初期化
        
        Args:
            user: Gmailユーザー名（Noneの場合はconfig.pyから読み込む）
            password: Gmailパスワード（Noneの場合はconfig.pyから読み込む）
            from_email: 送信元メールアドレス（Noneの場合はconfig.pyから読み込む）
            max_retries: 最大リトライ回数
            retry_delay: 初期リトライ間隔（秒）
            backoff_factor: バックオフ係数
        """
        self.user = user or EMAIL_USER
        self.password = password or EMAIL_PASS
        self.from_email = from_email or EMAIL_FROM or self.user
        
        if not self.user or not self.password:
            raise ValueError("ユーザー名またはパスワードが設定されていません。環境変数EMAIL_USERとEMAIL_PASSを設定するか、初期化時に指定してください。")
        
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
        
        logger.debug(f"GmailClientを初期化しました。ユーザー: {self.user}")
    
    def send_email(
        self, 
        to: Union[str, List[str]], 
        subject: str, 
        body: str,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        attachments: Optional[List[str]] = None,
        is_html: bool = False
    ) -> bool:
        """
        メールを送信する
        
        Args:
            to: 宛先メールアドレス（文字列または文字列のリスト）
            subject: 件名
            body: 本文
            cc: CC（文字列または文字列のリスト）
            bcc: BCC（文字列または文字列のリスト）
            attachments: 添付ファイルのパスのリスト
            is_html: HTMLメールかどうか
            
        Returns:
            bool: 送信成功したかどうか
        """
        retry_count = 0
        last_error = None
        current_delay = self.retry_delay
        
        # 宛先の処理
        if isinstance(to, str):
            to = [to]
        
        # CCの処理
        if cc is None:
            cc = []
        elif isinstance(cc, str):
            cc = [cc]
        
        # BCCの処理
        if bcc is None:
            bcc = []
        elif isinstance(bcc, str):
            bcc = [bcc]
        
        # 添付ファイルの処理
        if attachments is None:
            attachments = []
        
        while retry_count <= self.max_retries:
            try:
                logger.debug(f"メールを送信します。リトライ回数: {retry_count}")
                
                # メッセージの作成
                msg = MIMEMultipart()
                msg["From"] = self.from_email
                msg["To"] = ", ".join(to)
                msg["Cc"] = ", ".join(cc)
                msg["Subject"] = subject
                msg["Date"] = formatdate(localtime=True)
                
                # 本文の追加
                if is_html:
                    msg.attach(MIMEText(body, "html"))
                else:
                    msg.attach(MIMEText(body, "plain"))
                
                # 添付ファイルの追加
                for attachment in attachments:
                    try:
                        with open(attachment, "rb") as f:
                            part = MIMEApplication(f.read(), Name=attachment.split("/")[-1])
                        part["Content-Disposition"] = f'attachment; filename="{attachment.split("/")[-1]}"'
                        msg.attach(part)
                    except Exception as e:
                        logger.error(f"添付ファイルの追加に失敗しました: {e}")
                
                # SMTPサーバーに接続
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(self.user, self.password)
                    
                    # メールの送信
                    start_time = time.time()
                    server.send_message(msg)
                    end_time = time.time()
                    
                logger.debug(f"メールの送信が成功しました。所要時間: {end_time - start_time:.2f}秒")
                return True
                
            except Exception as e:
                # エラーの場合
                logger.warning(f"メール送信エラーが発生しました: {e}")
                last_error = e
                
                if retry_count < self.max_retries:
                    logger.info(f"{current_delay}秒後にリトライします。({retry_count+1}/{self.max_retries})")
                    time.sleep(current_delay)
                    current_delay *= self.backoff_factor  # バックオフ
                else:
                    logger.error(f"最大リトライ回数（{self.max_retries}回）を超えました。")
                    break
            
            retry_count += 1
        
        # 最大リトライ回数を超えた場合
        if last_error:
            logger.error(f"メールの送信に失敗しました: {last_error}")
        else:
            logger.error("不明なエラーが発生しました。")
        
        return False