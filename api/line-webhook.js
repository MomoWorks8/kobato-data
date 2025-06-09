// /api/line-webhook.js

const { Client, middleware } = require('@line/bot-sdk');
const getRawBody = require('raw-body');

const config = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.LINE_CHANNEL_SECRET,
};

const client = new Client(config);

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).end(); // Method Not Allowed
    return;
  }

  const rawBody = await getRawBody(req);
  const signature = req.headers['x-line-signature'];

  try {
    const events = middleware(config);
    await events(req, res, async () => {
      const body = JSON.parse(rawBody.toString());

      for (const event of body.events) {
        if (event.type === 'message' && event.message.type === 'text') {
          const msg = event.message.text.toLowerCase();
          if (msg.includes("くるっぽー")) {
            const reply = await fetch("https://kobato-data.vercel.app/api/kuruppo").then(res => res.text());
            await client.replyMessage(event.replyToken, {
              type: 'text',
              text: reply,
            });
          } else {
            await client.replyMessage(event.replyToken, {
              type: 'text',
              text: "ぽぽぽ？ もう一回くるっぽーって言ってみてぽ🕊️",
            });
          }
        }
      }

      res.status(200).send('OK');
    });
  } catch (err) {
    console.error("❌ LINE Webhook Error:", err);
    res.status(500).send("Internal Server Error");
  }
};
