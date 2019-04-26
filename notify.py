import os, smtplib, configparser

def initialize():
    if os.path.isfile('notify.config'):
        parameters = {}
        config = configparser.ConfigParser()
        config.read(os.getcwd() + '/notify.config')
        parameters['EMAIL'] = config.get('Config', 'email')
        parameters['PASSWORD'] = config.get('Config', 'password')
        parameters['SERVER'] = config.get('Config', 'server')
        parameters['PORT'] = config.get('Config', 'port')
        parameters['ADMIN'] = config.get('Admin', 'admin')
        parameters['SUBJECT'] = config.get('Message', 'subject')
        parameters['MESSAGE'] = config.get('Message', 'message')
        return parameters
    else:
        print('No configuration file.')

        
def notify(admin=[], msg=""):
    parameters = initialize()
    smtpObj = smtplib.SMTP(parameters['SERVER'], parameters['PORT'])
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(parameters['EMAIL'], parameters['PASSWORD'])
    
    if not msg:
        msg = parameters['MESSAGE']
    if not admin:
        admin.append(parameters['ADMIN'])
    
    smtpObj.sendmail(parameters['EMAIL'], admin, 'Subject:'+parameters['SUBJECT'] + '\n' + msg)              
    smtpObj.quit()

    
if __name__ == "__main__":
    notify('esgire@gmail.com', 'hello')