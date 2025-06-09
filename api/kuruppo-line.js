// kuruppo-line.js
import { middleware, Client } from '@line/bot-sdk';

const config = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.LINE_CHANNEL_SECRET,
};

const client = new Client(config);

// Main handler
export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      await middleware(config)(req, res, async () => {
        const events = req.body.events;

        const results = await Promise.all(events.map(async (event) => {
          if (event.type === 'message' && event.message.type === 'text') {
            const userMessage = event.message.text;

            if (userMessage.includes('くるっぽー')) {
              try {
                const response = await fetch('https://kobato-data.vercel.app/api/kuruppo');
                const message = await response.text();

                await client.replyMessage(event.replyToken, {
                  type: 'text',
                  text: message,
                });
              } catch (err) {
                console.error('API取得失敗:', err);
                await client.replyMessage(event.replyToken, {
                  type: 'text',
                  text: 'くるっぽーが空を飛びすぎて迷子ぽぽ…🕊️',
                });
              }
            } else {
              await client.replyMessage(event.replyToken, {
                type: 'text',
                text: 'ぽぽぽ？「くるっぽー」って言ってみてぽ🕊️',
              });
            }
          }
        }));

        res.status(200).send('OK');
      });
    } catch (err) {
      console.error('署名不正 or 例外:', err);
      res.status(500).send('エラーぽぽ');
    }
  } else {
    res.status(405).send('Method Not Allowed');
  }
}
