// /api/line-webhook.js

import { middleware, Client } from '@line/bot-sdk';

const config = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.LINE_CHANNEL_SECRET,
};

const client = new Client(config);

// ★ 必須：Vercelのエッジ関数形式でエクスポート
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Method Not Allowed');
  }

  try {
    const events = req.body.events;

    const results = await Promise.all(
      events.map(async (event) => {
        if (
          event.type === 'message' &&
          event.message.type === 'text' &&
          event.message.text.toLowerCase().includes('くるっぽー')
        ) {
          // 🔁 ここで Vercel の /api/kuruppo を叩く
          const response = await fetch('https://kobato-data.vercel.app/api/kuruppo');
          const text = await response.text();

          return client.replyMessage(event.replyToken, {
            type: 'text',
            text: text,
          });
        } else {
          return client.replyMessage(event.replyToken, {
            type: 'text',
            text: 'ぽぽぽ？もう一度「くるっぽー」って言ってみてぽ🕊️',
          });
        }
      })
    );

    res.status(200).json({ status: 'success', results });
  } catch (err) {
    console.error('❌ LINE webhook error:', err);
    res.status(500).send('Internal Server Error');
  }
}

// ★ LINE SDKミドルウェア対応（オプション）
export const config = {
  api: {
    bodyParser: false,
  },
};
