import { Box, Container, HStack } from '@chakra-ui/react';
import Chat from './components/Chat';
import Sidebar from './components/Sidebar';
import { useState } from 'react';

function App() {
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null);

  return (
    <Box bg="gray.900" h="100vh">
      <Container maxW="container.xl" h="full" p={4}>
        <HStack h="full" spacing={4} align="stretch">
          <Box w="300px" bg="gray.800" borderRadius="lg" boxShadow="lg">
            <Sidebar 
              selectedThreadId={selectedThreadId} 
              onSelectThread={setSelectedThreadId}
            />
          </Box>
          <Box flex={1} bg="gray.800" borderRadius="lg" boxShadow="lg">
            <Chat selectedThreadId={selectedThreadId} />
          </Box>
        </HStack>
      </Container>
    </Box>
  );
}

export default App;
