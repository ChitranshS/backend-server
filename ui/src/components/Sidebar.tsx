import { VStack, Button, Text, Box, IconButton, HStack } from '@chakra-ui/react';
import { AddIcon, DeleteIcon } from '@chakra-ui/icons';
import { useEffect, useState } from 'react';

interface Thread {
  id: string;
  name: string;
  lastMessage: string;
  timestamp: string;
}

interface SidebarProps {
  selectedThreadId: string | null;
  onSelectThread: (threadId: string) => void;
}

function Sidebar({ selectedThreadId, onSelectThread }: SidebarProps) {
  const [threads, setThreads] = useState<Thread[]>([]);

  useEffect(() => {
    const savedThreads = localStorage.getItem('chatThreads');
    if (savedThreads) {
      setThreads(JSON.parse(savedThreads));
    }
  }, []);

  const createNewThread = () => {
    // Generate a unique thread ID using timestamp and random number
    const threadId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const newThread: Thread = {
      id: threadId,
      name: `Chat ${threads.length + 1}`,
      lastMessage: 'New conversation',
      timestamp: new Date().toISOString(),
    };
    const updatedThreads = [newThread, ...threads];
    setThreads(updatedThreads);
    localStorage.setItem('chatThreads', JSON.stringify(updatedThreads));
    onSelectThread(newThread.id);
  };

  const deleteThread = (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const updatedThreads = threads.filter(thread => thread.id !== threadId);
    setThreads(updatedThreads);
    localStorage.setItem('chatThreads', JSON.stringify(updatedThreads));
    // Also remove the chat history for this thread
    localStorage.removeItem(`chat_history_${threadId}`);
    if (selectedThreadId === threadId) {
      onSelectThread(updatedThreads[0]?.id || null);
    }
  };

  const updateLastMessage = (threadId: string, message: string) => {
    const updatedThreads = threads.map(thread => 
      thread.id === threadId 
        ? { ...thread, lastMessage: message, timestamp: new Date().toISOString() } 
        : thread
    );
    setThreads(updatedThreads);
    localStorage.setItem('chatThreads', JSON.stringify(updatedThreads));
  };

  return (
    <VStack h="full" p={4} spacing={4} align="stretch">
      <Button
        leftIcon={<AddIcon />}
        colorScheme="blue"
        onClick={createNewThread}
        size="lg"
        w="full"
      >
        New Chat
      </Button>
      
      <VStack spacing={2} align="stretch" overflowY="auto">
        {threads.map((thread) => (
          <Box
            key={thread.id}
            p={3}
            bg={selectedThreadId === thread.id ? 'blue.700' : 'gray.700'}
            borderRadius="md"
            cursor="pointer"
            onClick={() => onSelectThread(thread.id)}
            _hover={{ bg: selectedThreadId === thread.id ? 'blue.600' : 'gray.600' }}
          >
            <HStack justify="space-between">
              <VStack align="start" spacing={1}>
                <Text fontWeight="bold" color="white">
                  {thread.name}
                </Text>
                <Text fontSize="sm" color="gray.300" noOfLines={1}>
                  {thread.lastMessage}
                </Text>
              </VStack>
              <IconButton
                icon={<DeleteIcon />}
                aria-label="Delete thread"
                size="sm"
                variant="ghost"
                colorScheme="red"
                onClick={(e) => deleteThread(thread.id, e)}
              />
            </HStack>
          </Box>
        ))}
      </VStack>
    </VStack>
  );
}

export default Sidebar;
