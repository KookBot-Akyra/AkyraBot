from akyrabot.khl import Bot, Message

runner = Bot(token='1/MjAyODI=/aIoIsYkIxGivVlqjObdKoA==')

@runner.command(name='hello')
async def world(msg: Message):
    await msg.reply('world!')

runner.run()
