const API_URL = 'http://localhost:3000/api';

class ApiService {
    async sendChatMessage(message) {
        try {
            console.log('Sending message to backend:', message);
            
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message })
            });

            const data = await response.json();
            
            if (!response.ok) {
                console.error('Server error details:', data);
                throw new Error(data.details || 'Server error occurred');
            }

            return data;
        } catch (error) {
            console.error('Chat API error:', error);
            throw error;
        }
    }
}

export default new ApiService(); 