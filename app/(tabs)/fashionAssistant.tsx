import { StyleSheet } from 'react-native';
import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';
import axios from 'axios';
import { GiftedChat, IMessage } from 'react-native-gifted-chat';
import React, { useState } from 'react';
import { TextInput} from 'react-native';
import { Button } from 'react-native-paper'; 

const ChatGPT35 = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const sendMessage = async () => {
    const userMessage = { role: 'user', content: inputText };
    setMessages([...messages, userMessage]);
    setInputText('');
    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-3.5-turbo',
          messages: [...messages, userMessage],
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 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',
          },
        }
      );
      const botMessage = {
        role: 'bot',
        content: response.data.choices[0].message.content,
      };
      setMessages([...messages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };
  return (
    <View>
      {messages.map((message, index) => (
        <Text key={index} style={{ color: message.role === 'user' ? 'blue' : 'green' }}>
          {message.content}
        </Text>
      ))}
      <TextInput
        style={{ height: 30, 
          borderColor: 'black', 
          borderWidth: 2, 
          top: 400 ,
          left: 8,
          borderRadius: 10,
        padding: 5, 
        width:360, 
        alignItems:'space-around'}}
        onChangeText={text => setInputText(text)}
        value={inputText}
      />
      <Button mode="contained"
        style={styles.sendbutton}
        buttonColor='lightskyblue'
        textColor='black'
        onPress={sendMessage} >
        Send
      </Button>
    </View>
  );
};
export default ChatGPT35;


const styles = StyleSheet.create({
  sendbutton:{
    position: 'absolute',
    top: 500,
    right: 150,
    alignItems: 'center'
  }

})