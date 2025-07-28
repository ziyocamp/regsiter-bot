from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from config import TOKEN, GENDER, PHOTO, LOCATION, BIO
from handlers import (
    start,
    gender,
    photo, skip_photo,
    location, skip_location,
    bio, 
    cancel,
)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],  # user create with id, first_name, last_name, username, ...
        states={
            GENDER: [MessageHandler(Filters.regex('^(Male|Female)$'), gender)], # user update and add gender
            PHOTO: [
                MessageHandler(Filters.photo, photo), # user update and add phone
                CommandHandler('skip', skip_photo)
            ],
            LOCATION: [
                MessageHandler(Filters.location, location), # user update and add location
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)], # user update and add bio
        },
        fallbacks=[CommandHandler('cancel', cancel)], # user delete
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
