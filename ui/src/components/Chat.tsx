import { useState, useRef, useEffect } from 'react';
import {
  VStack,
  Box,
  HStack,
  Text,
  useToast,
  IconButton,
  Textarea,
} from '@chakra-ui/react';
import { ArrowUpIcon } from '@chakra-ui/icons';
import axios from 'axios';
import { API_BASE_URL } from '../config';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

interface ChatProps {
  selectedThreadId: string | null;
}

function Chat({ selectedThreadId }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const toast = useToast();

  // Load chat history when thread changes
  useEffect(() => {
    if (selectedThreadId) {
      const savedMessages = localStorage.getItem(`chat_history_${selectedThreadId}`);
      if (savedMessages) {
        setMessages(JSON.parse(savedMessages));
      } else {
        setMessages([]);
      }
    } else {
      setMessages([]);
    }
  }, [selectedThreadId]);

  // Save chat history when messages change
  useEffect(() => {
    if (selectedThreadId && messages.length > 0) {
      localStorage.setItem(`chat_history_${selectedThreadId}`, JSON.stringify(messages));
      
      // Update the last message in the thread list
      const lastMessage = messages[messages.length - 1];
      const event = new CustomEvent('updateLastMessage', {
        detail: {
          threadId: selectedThreadId,
          message: lastMessage.content.substring(0, 50) + (lastMessage.content.length > 50 ? '...' : '')
        }
      });
      window.dispatchEvent(event);
    }
  }, [messages, selectedThreadId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async () => {
    if (!input.trim() || !selectedThreadId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        messages: input,
        thread_id: selectedThreadId
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.content,
        role: 'assistant',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to send message',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (!selectedThreadId) {
    return (
      <VStack h="full" justify="center" spacing={4} p={8}>
        <Text fontSize="xl" color="gray.400">
          Select a chat thread or create a new one to start messaging
        </Text>
      </VStack>
    );
  }

  return (
    <VStack h="full" spacing={4} bg="gray.800" p={4}>
      <Box
        flex={1}
        w="full"
        overflowY="auto"
        px={4}
        py={2}
        css={{
          '&::-webkit-scrollbar': {
            width: '4px',
          },
          '&::-webkit-scrollbar-track': {
            width: '6px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'gray',
            borderRadius: '24px',
          },
        }}
      >
        {messages.map((message) => (
          <Box
            key={message.id}
            bg={message.role === 'user' ? 'blue.700' : 'gray.700'}
            color="white"
            p={4}
            borderRadius="lg"
            mb={4}
            maxW="80%"
            ml={message.role === 'user' ? 'auto' : 0}
          >
            <Text whiteSpace="pre-wrap">{message.content}</Text>
            <Text
              fontSize="xs"
              color="gray.400"
              mt={1}
              textAlign={message.role === 'user' ? 'right' : 'left'}
            >
              {new Date(message.timestamp).toLocaleTimeString()}
            </Text>
          </Box>
        ))}
        <div ref={messagesEndRef} />
      </Box>
      <HStack w="full" spacing={2} p={2} bg="gray.700" borderRadius="lg">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSubmit()}
          resize="none"
          rows={1}
          bg="gray.600"
          color="white"
          _placeholder={{ color: 'gray.400' }}
          _hover={{ bg: 'gray.600' }}
          _focus={{ bg: 'gray.600', borderColor: 'blue.500' }}
        />
        <IconButton
          colorScheme="blue"
          aria-label="Send message"
          icon={<ArrowUpIcon />}
          onClick={handleSubmit}
          isLoading={isLoading}
          size="lg"
        />
      </HStack>
    </VStack>
  );
}

export default Chat;
