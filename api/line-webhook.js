// api/line-webhook.js
const { middleware, Client } = require('@line/bot-sdk');

const client = new Client({
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.LINE_CHANNEL_SECRET,
});

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).send('Method Not Allowed');
  }

  try {
    await middleware({ channelSecret: process.env.LINE_CHANNEL_SECRET })(req, res, async () => {
      const events = req.body.events;

      for (const event of events) {
        if (event.type === 'message' && event.message.type === 'text') {
          const msg = event.message.text;
          if (msg.includes('くるっぽー')) {
            const r = await fetch("https://kobato-data.vercel.app/api/kuruppo");
            const text = await r.text();
            await client.replyMessage(event.replyToken, { type: 'text', text });
          } else {
            await client.replyMessage(event.replyToken, {
              type: 'text',
              text: 'ぽ？小鳩ちゃんとお話しするときは、GPTのボタンを押してね🕊️',
            });
          }
        }
      }

      return res.status(200).end();
    });
  } catch (e) {
    console.error("💥 LINE Webhookエラー:", e);
    return res.status(500).send("Internal Server Error");
  }
};
