<script>
    import Navbar from '../../components/Navbar.svelte';
    import Footer from '../../components/Footer.svelte';
    import { fade, fly } from 'svelte/transition';
    import apiService from '$lib/services/api.js';

    let messages = [
        {
            type: 'system',
            content: 'Welcome to Bonker AI. Ask me anything about your finances.'
        }
    ];
    
    let chatHistory = [
        { id: 1, title: 'Spending Analysis', date: 'Today', active: true },
        { id: 2, title: 'Budget Review', date: 'Yesterday', active: false },
        { id: 3, title: 'Investment Strategy', date: 'Oct 24', active: false },
        { id: 4, title: 'Savings Goals', date: 'Oct 23', active: false },
    ];
    
    let inputMessage = '';
    let chatContainer;
    let isLoading = false;

    async function handleSubmit() {
        if (!inputMessage.trim() || isLoading) return;

        try {
            isLoading = true;
            console.log('Submitting message:', inputMessage);

            // Add user message
            messages = [...messages, {
                type: 'user',
                content: inputMessage
            }];

            // Send to backend
            const response = await apiService.sendChatMessage(inputMessage);
            console.log('Backend response:', response);

            // Add AI response
            messages = [...messages, {
                type: 'assistant',
                content: response.explanation || 'Sorry, I could not process that request.',
                data: response.results ? {
                    type: 'results',
                    sql: response.sql,
                    results: response.results
                } : null
            }];

            inputMessage = '';
        } catch (error) {
            console.error('Chat error:', error);
            messages = [...messages, {
                type: 'system',
                content: `Error: ${error.message || 'Something went wrong. Please try again.'}`
            }];
        } finally {
            isLoading = false;
            scrollToBottom();
        }
    }

    function scrollToBottom() {
        setTimeout(() => {
            chatContainer?.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }

    function startNewChat() {
        messages = [{
            type: 'system',
            content: 'Welcome to Bonker AI. Ask me anything about your finances.'
        }];
        chatHistory = chatHistory.map(chat => ({ ...chat, active: false }));
        chatHistory = [{ 
            id: Date.now(), 
            title: 'New Chat', 
            date: 'Just now', 
            active: true 
        }, ...chatHistory];
    }
</script>

<div class="flex flex-col min-h-screen bg-black">
    <Navbar />

    <main class="flex-1 pt-20">
        <div class="h-[calc(100vh-5rem)] flex">
            <!-- Sidebar -->
            <div class="w-80 border-r border-white/[0.05] backdrop-blur-xl bg-white/[0.02] p-4">
                <!-- New Chat Button -->
                <button 
                    on:click={startNewChat}
                    class="w-full bg-white hover:bg-white/90 text-black px-4 py-3 rounded-lg transition-colors flex items-center justify-center gap-2 mb-6"
                >
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
                    </svg>
                    <span>New Chat</span>
                </button>

                <!-- Chat History -->
                <div class="space-y-2">
                    <div class="text-white/40 text-sm px-2 mb-4">Chat History</div>
                    {#each chatHistory as chat}
                        <button 
                            class="w-full text-left p-3 rounded-lg transition-colors {chat.active ? 'bg-white/10' : 'hover:bg-white/[0.05]'}"
                        >
                            <div class="flex items-start gap-3">
                                <div class="w-8 h-8 rounded-lg bg-white/[0.05] flex items-center justify-center flex-shrink-0">
                                    <span class="text-white/70">💬</span>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <div class="text-white/90 text-sm truncate">{chat.title}</div>
                                    <div class="text-white/40 text-xs">{chat.date}</div>
                                </div>
                            </div>
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Chat Area -->
            <div class="flex-1 flex flex-col">
                <!-- Messages Area -->
                <div 
                    bind:this={chatContainer}
                    class="flex-1 overflow-y-auto p-6 messages-container"
                >
                    <div class="max-w-3xl mx-auto space-y-6">
                        {#each messages as message, i (i)}
                            <div 
                                in:fly={{ y: 20, duration: 300 }}
                                class="flex items-start gap-4"
                            >
                                <!-- Avatar -->
                                <div class="w-8 h-8 rounded-lg bg-white/[0.05] border border-white/[0.05] flex items-center justify-center flex-shrink-0">
                                    {#if message.type === 'user'}
                                        <span class="text-white/70">👤</span>
                                    {:else if message.type === 'assistant'}
                                        <span class="text-white/70">🤖</span>
                                    {:else}
                                        <span class="text-white/70">ℹ️</span>
                                    {/if}
                                </div>

                                <!-- Message Content -->
                                <div class="flex-1">
                                    <div class="bg-white/[0.03] rounded-2xl rounded-tl-none p-4">
                                        <p class="text-white/90 leading-relaxed">{message.content}</p>

                                        {#if message.data?.type === 'results'}
                                            <div class="mt-4 space-y-4">
                                                <div class="bg-white/[0.02] rounded-lg p-4">
                                                    <div class="text-white/40 text-sm mb-2">Generated SQL:</div>
                                                    <code class="text-white/90 text-sm font-mono">{message.data.sql}</code>
                                                </div>
                                                
                                                {#if message.data.results}
                                                    <div class="bg-white/[0.02] rounded-lg p-4">
                                                        <div class="text-white/40 text-sm mb-2">Results:</div>
                                                        <pre class="text-white/90 text-sm overflow-x-auto">
                                                            {JSON.stringify(message.data.results, null, 2)}
                                                        </pre>
                                                    </div>
                                                {/if}
                                            </div>
                                        {/if}
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Input Area -->
                <div class="border-t border-white/[0.05] backdrop-blur-xl bg-white/[0.02] p-4">
                    <div class="max-w-3xl mx-auto">
                        <form 
                            on:submit|preventDefault={handleSubmit}
                            class="flex items-center gap-4"
                        >
                            <input
                                bind:value={inputMessage}
                                type="text"
                                placeholder="Ask about your finances..."
                                class="flex-1 bg-white/[0.05] border border-white/[0.05] rounded-lg px-4 py-3 text-white/90 placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/10"
                            />
                            <button 
                                type="submit"
                                class="bg-white hover:bg-white/90 text-black px-6 py-3 rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={isLoading}
                            >
                                {#if isLoading}
                                    <div class="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                                {:else}
                                    <span>Send</span>
                                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7"/>
                                    </svg>
                                {/if}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </main>
</div>
<Footer />
<style>
    .messages-container::-webkit-scrollbar {
        display: none;
    }
    .messages-container {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style> 