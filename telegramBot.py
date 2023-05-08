from turtle import update
from telegram import Update,Bot
import telegram
from PIL import Image
from io import BytesIO
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.utils.request import Request
from telegram.ext import CallbackQueryHandler
import os,json
import requests
import re



#get api key from env

pwd="6244638575:AAFFOa2m6Fxz1PaxAL0OArIwTUHwSYiKJmU"
url="https://scizers-backend.vercel.app/shop"
bot=telegram.Bot(token=pwd)


username="User"
useremail="email"
userphone="phone"
useraddress="address"
firstmessage="Hello, "+username+"\nWelcome to our shopping bot! \nPlease Type Your Phone No. and Email in the given Format \U0001F447\n{Phone no.}\n{Email Id}\n{Address}\n\nSample-\n1234567890\nsk@gmail.com\nIIT Dhanbad 826004"




class productModel:
    def _init_(self,name,desc,image,count,price,aval):
        self.name=name
        self.desc=desc
        self.image=image
        self.count=count
        self.price=price
        self.aval=aval



class shopModel:
    def _init_(self,name,phone,payment,address,products):
        self.name=name
        self.phone=phone
        self.payment=payment
        self.address=address
        self.products=products
    def getname(self):    
        return self.name 
#array_shop=[shopModel("name1=22","8988","payment","address1",productModel("pname","desc","image","count","price","aval")),shopModel("name1","5677","payment","address1",productModel("pname","desc","image","count","price","aval")),shopModel("name1","5677","payment","address1",productModel("pname","desc","image","count","price","aval"))]



arrayShopdata=[]
array_shop=[]




#cart handling
my_cart={"Your Address- ":"address","Name- ":"name","Phone No.- ":"phone","Total Price- ":0}











curr_shop_index=0
curr_prod_index=0
curr_count=0
count_message=""








keyboard = [
        [InlineKeyboardButton("-1", callback_data='decrement'),
         InlineKeyboardButton("+1", callback_data='increment')],
        [InlineKeyboardButton("Confirm", callback_data='confirm1'),
         InlineKeyboardButton("Cancel", callback_data='cancel1')]
    ]
count_markup = InlineKeyboardMarkup(keyboard)



def count_button(update,context):
    global curr_count
    query = update.callback_query
    data = query.data
    if data == 'increment':
        if(int(array_shop[curr_shop_index]['products'][curr_prod_index]['count'])>curr_count):
          curr_count+=1
        query.edit_message_text(count_message+"- "+str(curr_count),reply_markup=count_markup)
    elif data == 'decrement':
        #curr_count+=1
        if(curr_count>0):
         curr_count-=1;
        query.edit_message_text(count_message+"- "+str(curr_count),reply_markup=count_markup)
    elif data == 'confirm1':
        #show cart
        query.edit_message_text("No. of "+array_shop[curr_shop_index]['products'][curr_prod_index]['name']+" "+'selected is : {}'.format(curr_count)+'\n\nTo see Your Cart /cart')
        my_cart[array_shop[curr_shop_index]['products'][curr_prod_index]['name']]=curr_count
        my_cart["Total Price in Rs- "]+=(int(array_shop[curr_shop_index]['products'][curr_prod_index]['price'])*curr_count)
        curr_count=0
    elif data == 'cancel1':
        #show cart
        query.edit_message_text('Cancelled. by User\n\nTo see Your Cart /cart')
    else:
        pass
count_handler=CallbackQueryHandler(count_button)

def callback_query_handler(update, context):
        
     context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F91D \n' )   
     #context.bot.send_message(chat_id=update.effective_chat.id,text=afterConfirmMessage )
     response=requests.get(url)
     if(response.status_code==200):
        array_shop.clear()
        my_cart={"Your Address- ":"address","Name- ":"name","Phone No.- ":"phone","Total Price in Rs- ":0}
        arrayShopdata=json.loads(response.text)
            #print(str(arrayShopdata))
        for item in arrayShopdata:
                my_model =item
                array_shop.append(my_model)
        print(str(array_shop))
        afterConfirmMessage="Welcome to our shopping bot! \nWe have a wide selection of products to choose from different Shop, including electronics, fashion, home goods, and more. \n\nTo get started Choose One Shop :\n\n"
        for i in range(len(array_shop)):
         model=array_shop[i]
         index=str(i+1)
         choose="choose"+str(i+1)
         print(model['name'])
         afterConfirmMessage+=index+". "+model['name']+"\n"+model['address']+"\n"+"\n\n"
         afterConfirmMessage+="Choose This Shop-  /"+choose+" \n\n\n"
        context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n' )
        afterConfirmMessage+=   "If you have any questions, just type /help for assistance\n"
        context.bot.send_message(chat_id=update.effective_chat.id,text=afterConfirmMessage )
     else:
        context.bot.send_message(chat_id=update.effective_chat.id,text="Network Error Try Again" )
print(str(array_shop))
button_pattern = re.compile('^option1\d+$')
button_handler=CallbackQueryHandler(callback_query_handler,pattern=button_pattern)




   



def start(update, context):
   # message = " Welcome to our General Store!\n For future Reference will you provide me your phone number\n Format- 1234567890,sk@gmail.com"
    user=update.message.from_user
    username=user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n\n' )
    context.bot.send_message(chat_id=update.effective_chat.id, text=firstmessage)
   








def error(update):
     bot.sendMessage(chat_id=update.effective_chat.id, text='Wrong Command!! Please Give /start to begin',disable_notification=False)
     return

def handle_message(update, context):
    message_text = update.message.text
    user_id = update.message.from_user.id
    
    if(len(message_text)<10):
        error(update)


    elif(len(message_text)<37 and len(message_text)>20):
        context.bot.send_message(chat_id=update.effective_chat.id,text="check Credential {"+message_text+"}" )
        context.bot.send_message(chat_id=update.effective_chat.id,text=firstmessage )

    else:
        temp_phone=message_text.split('\n',1)[0]
        userphone=temp_phone
        rem=message_text.split('\n',1)[1]
        
        temp_email=rem.split('\n',1)[0]
        useremail=temp_email
        rem=rem.split('\n',1)[1]

        temp_add=rem
        useraddress=temp_add
        print(len(temp_phone))
        if(temp_phone.isdigit() and len(temp_phone)==10):
          global button_handler
          button_pattern = re.compile('^option1\d+$')
          button_handler=CallbackQueryHandler(callback_query_handler,pattern=button_pattern)
          update.message.reply_text("Please Confirm your details and wait..  \n\nYour Email- "+temp_email+"\nYour Phone- "+temp_phone+"\nYour Address- "+temp_add)
          callback_query_handler(update,context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,text="check Phone Number {"+temp_phone+"}" )






























def choose1(update, context):
    if(len(array_shop)==0):error(update)
    if(len(array_shop)==0):error(update)
    msg="Here Are All the Product of "+array_shop[0]['name']+" :\n\n"
    msg+="Select One By One Among These Producs-\n"
    totalproduct=array_shop[0]['products']
    curr_shop_index=0
    for i in range(len(totalproduct)):
         model=totalproduct[i]
         index=str(i+1)
         choose="Click"+str(i+1)
         print(model['name'])
         msg+=index+". Name- "+model['name']+"\nDescription- "+model['desc']+"\ncount Remaining- "+model['count']+"\nPrice- "+model['price']+"\n\n"
         msg+="Choose This Product-  /"+choose+" \n\n\n"
   # context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n' )
    msg+=   "If you have any questions, just type /help for assistance\n"
    context.bot.send_message(chat_id=update.effective_chat.id,text=msg )



def choose2(update, context):
    if(len(array_shop)==0):error(update)
    msg="Here Are All the Product of "+array_shop[1]['name']+" :\n\n"
    totalproduct=array_shop[1]['products']
    curr_shop_index=1
    print(array_shop[1])
    for i in range(len(totalproduct)):
         model=totalproduct[i]
         index=str(i+1)
         choose="Click"+str(i+1)
         print(model['name'])
         msg+=index+". Name- "+model['name']+"\nDescription- "+model['desc']+"\ncount Remaining- "+model['count']+"\nPrice- "+model['price']+"\n\n"
         msg+="Choose This Product-  /"+choose+" \n\n\n"
   # context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n' )
    msg+=   "If you have any questions, just type /help for assistance\n"
    context.bot.send_message(chat_id=update.effective_chat.id,text=msg )


def choose3(update, context):
    if(len(array_shop)==0):error(update)
    msg="Here Are All the Product of "+array_shop[2]['name']+" :\n\n"
    totalproduct=array_shop[2]['products']
    curr_shop_index=2
    print(array_shop[1])
    for i in range(len(totalproduct)):
         model=totalproduct[i]
         index=str(i+1)
         choose="Click"+str(+i+1)
         print(model['name'])
         msg+=index+". Name- "+model['name']+"\nDescription- "+model['desc']+"\ncount Remaining- "+model['count']+"\nPrice- "+model['price']+"\n\n"
         msg+="Choose This Product-  /"+choose+" \n\n\n"
   # context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n' )
    msg+=   "If you have any questions, just type /help for assistance\n"
    context.bot.send_message(chat_id=update.effective_chat.id,text=msg )


def choose4(update, context):
    if(len(array_shop)==0):error(update)
    msg="Here Are All the Product of "+array_shop[3]['name']+" :\n\n"
    totalproduct=array_shop[3]['products']
    curr_shop_index=3
    print(array_shop[1])
    for i in range(len(totalproduct)):
         model=totalproduct[i]
         index=str(i+1)
         choose="Click"+str(+i+1)
         print(model['name'])
         msg+=index+". Name- "+model['name']+"\nDescription- "+model['desc']+"\ncount Remaining- "+model['count']+"\nPrice- "+model['price']+"\n\n"
         msg+="Choose This Product-  /"+choose+" \n\n\n"
   # context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n' )
    msg+=   "If you have any questions, just type /help for assistance\n"
    context.bot.send_message(chat_id=update.effective_chat.id,text=msg )

def choose5(update, context):
    if(len(array_shop)==0):error(update)
    msg="Here Are All the Product of "+array_shop[4]['name']+" :\n\n"
    totalproduct=array_shop[4]['products']
    curr_shop_index=4
    print(array_shop[1])
    for i in range(len(totalproduct)):
         model=totalproduct[i]
         index=str(i+1)
         choose="Click"+str(+i+1)
         print(model['name'])
         msg+=index+". Name- "+model['name']+"\nDescription- "+model['desc']+"\ncount Remaining- "+model['count']+"\nPrice- "+model['price']+"\n\n"
         msg+="Choose This Product-  /"+choose+" \n\n\n"
   # context.bot.send_message(chat_id=update.effective_chat.id,text='\U0001F64F \n' )
    msg+=   "If you have any questions, just type /help for assistance\n"
    context.bot.send_message(chat_id=update.effective_chat.id,text=msg )




def updateMsg(update,curr_shop_index,curr_prod_index):
    if(len(array_shop)==0):error(update)
    print("click11")
    global count_message
    count_message="Select Quantity Here-> \n\n"+array_shop[curr_shop_index]['products'][curr_prod_index]['name']+" "
    bot.send_photo(chat_id=update.effective_chat.id,photo=array_shop[curr_shop_index]['products'][curr_prod_index]['image'],caption="Branded!! You Can Trust On our "+array_shop[curr_shop_index]['products'][curr_prod_index]['name'])
    return update.message.reply_text(count_message, reply_markup=count_markup)
   # return bot.send_photo(chat_id=update.effective_chat.id,photo=array_shop[curr_shop_index]['products'][curr_prod_index]['image'],caption=count_message,reply_markup=count_markup)


def click1(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_shop_index=0
    curr_prod_index=0
    updateMsg(update,curr_shop_index,curr_prod_index)

def click2(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=1
    updateMsg(update,curr_shop_index,curr_prod_index)  

def click3(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=2
    updateMsg(update,curr_shop_index,curr_prod_index)  

def click4(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=3
    updateMsg(update,curr_shop_index,curr_prod_index)

def click5(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=4
    updateMsg(update,curr_shop_index,curr_prod_index)  

def click6(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=5
    updateMsg(update,curr_shop_index,curr_prod_index) 

def click7(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=6
    updateMsg(update,curr_shop_index,curr_prod_index)

def click8(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=7
    updateMsg(update,curr_shop_index,curr_prod_index)  

def click9(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=8
    updateMsg(update,curr_shop_index,curr_prod_index) 

def click10(update, context):
    if(len(array_shop)==0):error(update)
    global curr_prod_index,curr_shop_index
    curr_prod_index=9
    updateMsg(update,curr_shop_index,curr_prod_index)

def Home(update,context):
    if(len(array_shop)==0):
        error(update)
        return
    callback_query_handler(update,context)

def help(update,context):
    if(len(array_shop)==0):error(update)
    msg="All the helpful command and chat facility with the admin will be available if needed"
    context.bot.send_message(chat_id=update.effective_chat.id,text=msg )

    
my_cart={"Your Address- ":"address","Name- ":"name","Phone No.- ":"phone","Total Price in Rs- ":0}
def Remove(update,context):
    global my_cart

    if(len(array_shop)==0):error(update)
    my_cart.clear()
    my_cart={"Your Address- ":"address","Name- ":"name","Phone No.- ":"phone","Total Price in Rs- ":0}
    











orders_summary="\nOrder Summary:- \n"
def cart(update,context):
    global orders_summary
    orders="Your Selected Items:- \n"
    details="Welcome To Your Cart\n\n"
    for key, value in my_cart.items():
        kk=str(key)
        if(kk[len(kk)-1]!=' '):
            orders+=kk
            orders_summary+=kk
            orders+=":- "
            orders_summary+=":- "
            orders+=str(value)
            orders_summary+=str(value)
            orders+='\n'
            orders_summary+='\n'
        else:
            details+=kk
            details+=str(value)
            details+="\n"
    orders+='\n'
    orders_summary+='\n'
    details+='\n'
    orders+="For Placing Order click /Place_Order\n\n"
    orders+="Go to /Home\n"
    orders+="Remove all The Items and Make a New Cart \n/Remove\n"
    msg=details+orders
    
    #bot.send_photo(chat_id=update.effective_chat.id, photo='https://purepng.com/public/uploads/large/purepng.com-shopping-cartshoppingcarttrolleycarriagebuggysupermarkets-14215265325036jrux.png')
    photo="https://i.ebayimg.com/images/g/nbMAAOSwdHlf0XMN/s-l300.png"
    context.bot.send_photo(chat_id=update.effective_chat.id,photo=photo,caption=msg )







def place_order(update,context):
     photo=array_shop[curr_shop_index]['payment']
     context.bot.send_photo(chat_id=update.effective_chat.id,photo=photo,caption="Scan Here and Pay Rs."+str(my_cart['Total Price in Rs- '])+" for Your Order!!!\n"+orders_summary+" \nSend The ScreenShot Shopkeeper will verify and inform you.\nWe will try our best so that our delivery partner will reach you As Soon As Possible\nCancel Order and go to /Home" )







def main():
    req=Request(con_pool_size=10,connect_timeout=0.5)
    t_bot=Bot(request=req,token=pwd)
    updater=Updater(bot=t_bot,use_context=True)
    dp=updater.dispatcher

    start_handler = CommandHandler("start", start)
    dp.add_handler(start_handler)

    browse_handler = CommandHandler("choose1", choose1)
    dp.add_handler(browse_handler)

    browse_handler2 = CommandHandler("choose2", choose2)
    dp.add_handler(browse_handler2)

    browse_handler3 = CommandHandler("choose3", choose3)
    dp.add_handler(browse_handler3)

    browse_handler4 = CommandHandler("choose4", choose4)
    dp.add_handler(browse_handler4)

    cart_ha=CommandHandler("cart",cart)
    dp.add_handler(cart_ha)

    click11_ha=CommandHandler("Click1",click1)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click2",click2)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click3",click3)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click4",click4)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click5",click5)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click6",click6)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click7",click7)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click8",click8)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click9",click9)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Click10",click10)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("place_order",place_order)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Home",Home)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("help",help)
    dp.add_handler(click11_ha)

    click11_ha=CommandHandler("Remove",Remove)
    dp.add_handler(click11_ha)
    
    dp.add_handler(CallbackQueryHandler(count_button))
    
    # Register the handlers for button clicks
    
   


   

    dp.add_handler(MessageHandler(filters=Filters.all,callback=handle_message))
    #dp.add_handler(CallbackQueryHandler(callback_query_handler,pattern='^confirm_pattern_'))
   



    updater.start_polling()
    updater.idle()

    
    #dp.add_handler(MessageHandler(filters=Filters.all,callback=message_handler))
    

if _name=="__main_":
    main()