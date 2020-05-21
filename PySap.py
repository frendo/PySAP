#-Begin-----------------------------------------------------------------

#-Includes--------------------------------------------------------------
import sys, win32com.client
import logging

#-Sub Main--------------------------------------------------------------
def sap_connect():
    logging.info('Runnning sap_connect()')
    try:
        response = ''
        while response != 'exit':
            try:

                SapGuiAuto = win32com.client.GetObject("SAPGUI")
                if not type(SapGuiAuto) == win32com.client.CDispatch:
                    logging.error('SapGuiAuto')
                    return

                application = SapGuiAuto.GetScriptingEngine

                if not type(application) == win32com.client.CDispatch:
                    logging.error('Application')
                    SapGuiAuto = None
                    return

                connection = application.Children(0)
                if not type(connection) == win32com.client.CDispatch:
                    logging.error('Connection')
                    application = None
                    SapGuiAuto = None
                    return

                session = connection.Children(0)
                if not type(session) == win32com.client.CDispatch:
                    logging.error('Session')
                    connection = None
                    application = None
                    SapGuiAuto = None
                    return
                else:
                    logging.info('Session connected')
                    return session

            except:
                logging.info('Requesting user action - no sap window')
                response = input("Please open sap and click return when ready or type 'exit' to exit the program: ")
            finally:
                connection = None
                application = None
                SapGuiAuto = None
                logging.info('exit from function')

    except:
        print(sys.exc_info()[0])

def read_table(session):
    logging.info('Running read_table(session)')
    try:
        
        wnd = session.findById("wnd[0]")
        tbar = session.findById("wnd[0]/tbar[0]/okcd")
        sbar = session.FindById("wnd[0]/sbar")

        wnd.resizeWorkingPane(173, 36, 0)
        tbar.text = "/nse16"
        wnd.sendVKey(0)
        session.findById("wnd[0]/usr/ctxtDATABROWSE-TABLENAME").text = "ANKA"
        wnd.sendVKey(0)
        #session.findById("wnd[0]/tbar[1]/btn[8]").press
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        print(sbar.text)
    except:
        print(sys.exc_info()[0])

    finally:
        session = None
        wnd = None
        tbar = None
        sbar = None

#-Main------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    session = sap_connect()
    read_table(session)
#-End-------------------------------------------------------------------