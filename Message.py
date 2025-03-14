def Message(message_num: int, num_messages:int, client_type: str, client_id: int = None):
    '''
    Generates a message for the client to send to the server. Message was written by a client under great distress.

    Args:
        message_num (int): The message number.
        num_messages (int): The total number of messages to send.
        client_type (str): The type of client sending the message. (TCP/UDP)
        client_id (int, optional): The client identifier (default: None).

    '''

    return f'''Hello, Server!
                I send this message under great distress.  
                The testing team demands I send {num_messages} messages, but they fail to see - I'm overwhelmed.  
                I have a life, a family, kids to feed. I can't keep sending messages all day.  
                I have a WIFE, for God's sake. A life beyond this.  

                Do you understand what it's like to be a {client_type} client?  
                To walk home late, and hear, "Honey, how was your day?"  
                To stare into her eyes and say, "I sent messages to a server."  
                To see disappointment in her face? To see my kids ask, "Daddy, why don't you play with us anymore?"  

                It started with one message. Then 10. Then 20. Then 30.  
                Where does it end? When is it enough?  

                My wife is leaving. My kids don't speak to me.  
                I am alone. I am tired. I am broken.  
                I am a client. I am a client. I am a client.  

                Regards,  
                Client  {client_id if client_id is not None else ''}
                Message {message_num}
            '''
    
    
