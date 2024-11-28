<script>
    import Navbar from '../../components/Navbar.svelte';
    import Footer from '../../components/Footer.svelte';
    import { fade, fly } from 'svelte/transition';
    import apiService from '$lib/services/api.js';

    let messages = [
        {
            type: 'system',
            content: 'Ask me anything about your finances.'
        }
    ];
    
    let inputMessage = '';
    let chatContainer;
    let isLoading = false;
    let showSidebar = true;

    const sampleQueries = [
        "Show my total expenses by category this month",
        "What's my income vs expenses ratio?",
        "Show my highest spending categories",
        "Calculate my monthly savings rate"
    ];

    function startNewChat() {
        messages = [
            {
                type: 'system',
                content: 'Ask me anything about your finances.'
            }
        ];
    }

    async function handleSubmit() {
        if (!inputMessage.trim() || isLoading) return;
        isLoading = true;

        messages = [...messages, {
            type: 'user',
            content: inputMessage
        }];

        try {
            const response = await apiService.sendChatMessage(inputMessage);
            messages = [...messages, {
                type: 'assistant',
                content: response.explanation || 'Sorry, I could not process that request.',
                data: response.results ? {
                    type: 'results',
                    sql: response.sql,
                    results: response.results
                } : null
            }];
        } catch (error) {
            messages = [...messages, {
                type: 'system',
                content: `Error: ${error.message || 'Something went wrong'}`
            }];
        } finally {
            inputMessage = '';
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
</script>

<div class="min-h-screen bg-black flex flex-col">
    <Navbar />
    
    <div class="flex-1 flex h-[calc(100vh-64px)] pt-16">
        <!-- Sidebar -->
        <aside class="w-80 border-r border-white/10 flex-shrink-0 {showSidebar ? '' : 'hidden'} bg-black/30">
            <div class="h-full flex flex-col p-6">
                <!-- New Chat Button -->
                <button 
                    on:click={startNewChat}
                    class="w-full px-4 py-2.5 mb-8 rounded-lg bg-white/10 hover:bg-white/[0.15] text-white/90 text-sm font-medium transition-colors"
                >
                    New Chat
                </button>

                <!-- Sample Queries -->
                <div class="mb-8">
                    <h3 class="text-xs text-white/40 font-medium uppercase tracking-wider mb-4 px-4">Sample Queries</h3>
                    <div class="space-y-2.5">
                        {#each sampleQueries as query}
                            <button 
                                on:click={() => inputMessage = query}
                                class="w-full text-left px-4 py-2.5 rounded-lg text-white/60 text-sm hover:bg-white/[0.05] transition-colors"
                            >
                                {query}
                            </button>
                        {/each}
                    </div>
                </div>

                <!-- Recent Chats -->
                <div class="flex-1 overflow-y-auto">
                    <h3 class="text-xs text-white/40 font-medium uppercase tracking-wider mb-4 px-4">Recent Chats</h3>
                    <div class="space-y-2.5">
                        <button class="w-full text-left px-4 py-2.5 rounded-lg text-white/60 text-sm hover:bg-white/[0.05] transition-colors">
                            Monthly Analysis
                        </button>
                        <button class="w-full text-left px-4 py-2.5 rounded-lg text-white/60 text-sm hover:bg-white/[0.05] transition-colors">
                            Expense Categories
                        </button>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Chat Area with adjusted positioning -->
        <main class="flex-1 flex flex-col bg-black/30 relative">
            <!-- Toggle Sidebar Button with adjusted top position -->
            <button 
                on:click={() => showSidebar = !showSidebar}
                class="absolute left-4 top-6 p-2 rounded-lg hover:bg-white/[0.05] text-white/40 hover:text-white/60 transition-colors"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
            </button>

            <!-- Chat Messages with adjusted top margin -->
            <div 
                bind:this={chatContainer}
                class="flex-1 overflow-y-auto px-4 lg:px-8 py-6 space-y-6 mt-16"
            >
                {#each messages as message, i}
                    <div 
                        in:fly={{ y: 20, duration: 300, delay: i * 50 }}
                        class="max-w-3xl mx-auto flex items-start gap-4 {message.type === 'user' ? 'justify-end' : ''}"
                    >
                        {#if message.type !== 'user'}
                            <div class="w-2 h-2 rounded-full bg-white/20 mt-3"></div>
                        {/if}
                        
                        <div class="max-w-[85%]">
                            <div class="rounded-2xl p-4 {
                                message.type === 'user' 
                                    ? 'bg-white/10' 
                                    : message.type === 'system'
                                        ? 'bg-white/[0.02] border border-white/10'
                                        : 'bg-white/[0.05]'
                            }">
                                <p class="text-white/90 text-sm leading-relaxed">{message.content}</p>

                                {#if message.data?.type === 'results'}
                                    <div class="mt-4 space-y-3">
                                        <div class="bg-black/30 rounded p-3">
                                            <div class="text-white/40 text-xs mb-2 uppercase tracking-wider">Query</div>
                                            <code class="text-white/80 text-xs font-mono">{message.data.sql}</code>
                                        </div>
                                        
                                        {#if message.data.results?.length}
                                            <div class="bg-black/30 rounded p-3 overflow-x-auto">
                                                <div class="text-white/40 text-xs mb-2 uppercase tracking-wider">Results</div>
                                                <table class="w-full text-left">
                                                    <thead>
                                                        <tr>
                                                            {#each Object.keys(message.data.results[0]) as header}
                                                                <th class="p-2 text-white/40 text-xs uppercase">{header}</th>
                                                            {/each}
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {#each message.data.results as row}
                                                            <tr class="border-t border-white/[0.03]">
                                                                {#each Object.values(row) as cell}
                                                                    <td class="p-2 text-white/80 text-sm">{cell}</td>
                                                                {/each}
                                                            </tr>
                                                        {/each}
                                                    </tbody>
                                                </table>
                                            </div>
                                        {/if}
                                    </div>
                                {/if}
                            </div>
                        </div>
                    </div>
                {/each}

                {#if isLoading}
                    <div class="max-w-3xl mx-auto flex items-center gap-2">
                        <div class="w-1.5 h-1.5 rounded-full bg-white/40 animate-pulse"></div>
                        <div class="w-1.5 h-1.5 rounded-full bg-white/40 animate-pulse delay-75"></div>
                        <div class="w-1.5 h-1.5 rounded-full bg-white/40 animate-pulse delay-150"></div>
                    </div>
                {/if}
            </div>

            <!-- Input Area -->
            <div class="border-t border-white/10 bg-black/40 backdrop-blur-xl p-4">
                <div class="max-w-3xl mx-auto">
                    <form 
                        on:submit|preventDefault={handleSubmit}
                        class="relative"
                    >
                        <input
                            bind:value={inputMessage}
                            type="text"
                            placeholder="Ask about your finances..."
                            class="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white/90 text-sm placeholder:text-white/20 focus:outline-none focus:border-white/20 transition-colors"
                        />
                        <button 
                            type="submit"
                            disabled={isLoading}
                            class="absolute right-3 top-1/2 -translate-y-1/2 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs text-white/90 disabled:opacity-50 transition-colors"
                        >
                            Send
                        </button>
                    </form>
                </div>
            </div>
        </main>
    </div>
</div>
<Footer/>
<style>
    /* Hide scrollbar but maintain functionality */
    :global(.no-scrollbar) {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
    :global(.no-scrollbar::-webkit-scrollbar) {
        display: none;
    }
</style> 