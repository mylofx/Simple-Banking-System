import random
import sqlite3
from sqlite3 import Error


try:
    conn = sqlite3.connect('card.s3db')
except Error as e:
    print(e)
cur = conn.cursor()

try:
    cur.execute('CREATE TABLE card(id integer, number text, pin text, balance integer)')
except:
    pass
conn.commit()
class CardBank:
    recovery = False
    all_cards = []
    id_uni = 1
    def __init__(self):
        self.id = CardBank.id_uni
        CardBank.id_uni += 1
        self.card_number = '400000' + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))+ str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
        self.check_sum = 0
        x = 15
        for i in self.card_number:
            i = int(i)
            if x % 2 != 0:
                i *= 2
            if i > 9:
                i -= 9
            self.check_sum += i
            x -= 1
        if self.check_sum % 10 == 0:
            self.check_sum = 0
        else:
            self.check_sum = 10 - self.check_sum % 10
        self.card_number += str(self.check_sum)
        self.card_number = int(self.card_number)
        self.pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
        self.balance = 0
        if CardBank.recovery:
            print("""Your card has been created
Your card number:""")
            print(self.card_number)
            print("Your card PIN:")
            print(self.pin)
            CardBank.all_cards.append(self)
            cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?)', (self.id, self.card_number, self.pin, self.balance))
            conn.commit()

off = False
logged = False

def recover():
    CardBank.all_cards = []
    CardBank.recovery = False
    xxd = '1'
    cur.execute("SELECT * From card")
    arasiz = cur.fetchall()
    for i in range(len(arasiz)):
        xxd = str(xxd)
        new_recover = CardBank()
        cur.execute('SELECT number FROM card WHERE id = ?', (xxd,))
        new_recover.card_number = cur.fetchone()[0]
        cur.execute('SELECT pin FROM card WHERE id = ?', (xxd,))
        new_recover.pin = cur.fetchone()[0]
        cur.execute('SELECT balance FROM card WHERE id = ?', (xxd,))
        new_recover.balance = cur.fetchone()[0]
        CardBank.all_cards.append(new_recover)
        xxd = int(xxd)
        xxd += 1
    CardBank.recovery = True


recover()

while off == False:

    if logged == False:
        print("""1. Create an account
2. Log into account
0. Exit""")
        inxput = input()
        if inxput == '1':
            new_card = CardBank()
        elif inxput == '2':
            print('Enter your card number:')
            loginnumber = int(input())
            print("Enter your PIN:")
            loginpin = input()
            for logincard in CardBank.all_cards:
                if loginnumber == int(logincard.card_number) and loginpin == str(logincard.pin):
                    logged = True
                    print('You have successfully logged in!')
                    break
            else:
                print('Wrong card number or PIN!')
        elif inxput == '0':
            off = True
    else:
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        inxpu2 = input()
        if inxpu2 == '1':
            print('Balance:',  logincard.balance)
        elif inxpu2 == '0':
            off = True
        elif inxpu2 == '5':
            logged = False
            print('You have successfully logged out!')
        elif inxpu2 == '2':
            print('Enter income:')
            logincard.balance += int(input())
            cur.execute('update card set balance = ? where number = ?', (logincard.balance, logincard.card_number))
            conn.commit()
            print('Income was added!')
            recover()
        elif inxpu2 == '3':
            print('Enter card number:')
            transfer_card = int(input())
            luhn = 0
            luhn_index = 15
            for luchned in str(transfer_card):
                luchned = int(luchned)
                if luhn_index % 2 != 0:
                    luchned *= 2
                if luchned > 9:
                    luchned -= 9
                luhn += luchned
                luhn_index -= 1
            if luhn % 10 == 0 and int(transfer_card) != int(logincard.card_number):
                transaaction = True

                try:
                    cur.execute('select number from card where number = ?', (str(transfer_card),))
                    checking_nb = cur.fetchone()[0]

                except:
                        print('Such a card does not exist.')
                        transaaction = False
                finally:
                    if transaaction == True:
                        print('Enter how much money you want to transfer:')
                        transfer_money = int(input())
                        cur.execute('select balance from card where number = ?', (str(logincard.card_number),))
                        logincard.balance = cur.fetchone()[0]
                        if transfer_money > logincard.balance:
                            print('Not enough money!')
                        else:
                            logincard.balance -= transfer_money
                            cur.execute('select balance from card where number = ?', (str(transfer_card),))
                            transfer_balance = cur.fetchone()[0]
                            transfer_balance = int(transfer_balance) + transfer_money
                            cur.execute('update card set balance = ? where number = ?', (str(logincard.balance), str(logincard.card_number) ))
                            cur.execute('update card set balance = ? where number = ?', (str(transfer_balance), str(transfer_card)))
                            conn.commit()
                            print('Success!')
                            recover()

            elif transfer_card == int(logincard.card_number):
                print("You can't transfer money to the same account!")
            else:
                print('Probably you made a mistake in the card number. Please try again!')

        elif inxpu2 == '4':
            conn.execute('DELETE FROM card WHERE number = ?',((logincard.card_number,)))
            print('The account has been closed!')
            logged = False
            conn.commit()
            recover()
conn.commit()
conn.close()
print('Bye!')

