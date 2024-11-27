<script>
    import Navbar from '../components/Navbar.svelte';
    import Footer from '../components/Footer.svelte';
    import { fade, fly } from 'svelte/transition';

    let heroVisible = true;
</script>

<Navbar />

<!-- Hero Section -->
<section class="min-h-[90vh] bg-black pt-20 relative overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/[0.03] via-transparent to-transparent"></div>
    
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 pt-20">
        {#if heroVisible}
        <div in:fade={{ duration: 1000 }} class="relative">
            <!-- Subtle Label -->
            

            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div>
                    <h1 class="text-5xl sm:text-6xl text-white/90 leading-tight tracking-[-0.02em] mb-8">
                        Banking smarter with natural language
                    </h1>
                    
                    <p class="text-lg text-white/50 leading-relaxed mb-12 max-w-xl">
                        Transform your financial experience with AI-powered insights. Ask questions, get answers, and make informed decisions effortlessly.
                    </p>

                    <div class="flex flex-col sm:flex-row items-start gap-4 mb-16">
                        <a href="/chat" class="w-full sm:w-auto group flex items-center gap-3 text-white border border-white/10 hover:border-white/20 backdrop-blur-sm bg-white/5 hover:bg-white/10  px-8 py-4 rounded-lg font-medium transition-all duration-200 shadow-lg shadow-white/20">
                            <span>Get Started</span>
                            <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                            </svg>
                        </a>
                    </div>

                    <!-- Trust Indicators -->
                    <div class="flex flex-wrap items-center gap-8 text-white/40 text-sm">
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                            </svg>
                            <span>Bank-grade security</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                            </svg>
                            <span>Real-time analytics</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            <span>FDIC Insured</span>
                        </div>
                    </div>
                </div>

                <!-- Hero Visual -->
                <div class="relative hidden lg:block">
                    <div class="absolute inset-0 bg-gradient-to-tr from-white/[0.03] to-transparent rounded-2xl"></div>
                    <div class="backdrop-blur-xl bg-white/[0.02] border border-white/[0.05] rounded-2xl p-8">
                        <!-- Mock Banking Interface -->
                        <div class="space-y-8">
                            <!-- Balance Card -->
                            <div class="bg-gradient-to-r from-white/[0.05] to-white/[0.02] rounded-xl p-6 border border-white/[0.05]">
                                <div class="text-sm text-white/40 mb-2">Available Balance</div>
                                <div class="text-3xl text-white/90">$24,563.82</div>
                                <div class="mt-4 flex items-center gap-2 text-green-400/90 text-sm">
                                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                                    </svg>
                                    <span>+2.4% this month</span>
                                </div>
                            </div>

                            <!-- Quick Actions -->
                            <div class="grid grid-cols-3 gap-4">
                                {#each ['Send', 'Receive', 'Exchange'] as action}
                                    <div class="bg-white/[0.02] hover:bg-white/[0.04] border border-white/[0.05] rounded-lg p-4 text-center cursor-pointer transition-colors">
                                        <div class="text-white/90 text-sm">{action}</div>
                                    </div>
                                {/each}
                            </div>

                            <!-- Recent Activity -->
                            <div>
                                <div class="text-sm text-white/40 mb-4">Recent Activity</div>
                                {#each [
                                    { name: 'Apple Music', amount: '-$9.99', date: 'Today' },
                                    { name: 'Salary Deposit', amount: '+$4,400', date: 'Yesterday' },
                                    { name: 'Amazon', amount: '-$124.33', date: 'Oct 24' }
                                ] as tx}
                                    <div class="flex items-center justify-between py-3 border-b border-white/[0.05]">
                                        <div>
                                            <div class="text-white/80 text-sm">{tx.name}</div>
                                            <div class="text-white/40 text-xs">{tx.date}</div>
                                        </div>
                                        <div class="text-white/90 text-sm">{tx.amount}</div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {/if}
    </div>
</section>

<!-- Features Section -->
<section class="py-32 bg-black relative" id="features">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-3 gap-16">
            <!-- Feature Description -->
            <div class="lg:col-span-1">
                <div class="sticky top-32">
                    <div class="text-white/40 text-sm tracking-wider mb-4">FEATURES</div>
                    <h2 class="text-3xl text-white/90 leading-tight tracking-[-0.02em] mb-6">
                        Intelligence meets simplicity
                    </h2>
                    <p class="text-white/50 leading-relaxed">
                        Experience banking that understands you. Natural language processing meets financial expertise.
                    </p>
                </div>
            </div>

            <!-- Feature Cards -->
            <div class="lg:col-span-2 space-y-8">
                {#each [
                    {
                        title: "Natural Conversations",
                        description: "Ask about your finances in plain English. Get instant, intelligent responses powered by AI.",
                        
                    },
                    {
                        title: "Predictive Analytics",
                        description: "Understand spending patterns and receive personalized recommendations for better financial decisions.",
                        
                    },
                    {
                        title: "Smart Automation",
                        description: "Set intelligent rules based on your preferences. Let AI handle the routine while you focus on what matters.",
                        
                    }
                ] as feature, i}
                    <div 
                        in:fly={{ y: 20, duration: 1000, delay: i * 100 }}
                        class="group backdrop-blur-xl bg-white/[0.02] hover:bg-white/[0.04] border border-white/[0.05] rounded-xl p-8 transition-all duration-300"
                    >
                        <div class="flex items-start gap-6">
                            
                            <div>
                                <h3 class="text-xl text-white/90 mb-3">{feature.title}</h3>
                                <p class="text-white/50 leading-relaxed">{feature.description}</p>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</section>

<!-- Demo Section -->
<section class="py-32 bg-black relative" id="demo">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
            <!-- Demo Visual -->
            <div class="backdrop-blur-xl bg-white/[0.02] border border-white/[0.05] rounded-2xl p-8">
                <div class="space-y-6">
                    <!-- Chat Interface -->
                    <div class="space-y-4">
                        <div class="flex items-start gap-4">
                            <div class="flex-1">
                                <div class="bg-white/[0.02] rounded-2xl rounded-tl-none p-4">
                                    <p class="text-white/90">Show me my spending trends for dining out</p>
                                </div>
                            </div>
                        </div>

                        <div class="flex items-start gap-4">
                            <div class="flex-1">
                                <div class="bg-white/[0.04] rounded-2xl rounded-tr-none p-4">
                                    <p class="text-white/90 mb-4">Here's your dining expenses analysis:</p>
                                    
                                    <!-- Mock Chart -->
                                    <div class="h-48 flex items-end gap-2 mb-4">
                                        {#each [40, 65, 45, 80, 55, 70] as height}
                                            <div class="flex-1 bg-gradient-to-t from-white/[0.1] to-white/[0.02] rounded-t"
                                                 style="height: {height}%"></div>
                                        {/each}
                                    </div>

                                    <div class="text-sm text-white/60">
                                        Your dining expenses increased by 15% this month. Most frequent visits: Starbucks, Chipotle.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Demo Description -->
            <div>
                <div class="text-white/40 text-sm tracking-wider mb-4">HOW IT WORKS</div>
                <h2 class="text-3xl text-white/90 leading-tight tracking-[-0.02em] mb-6">
                    Banking that speaks your language
                </h2>
                <p class="text-white/50 leading-relaxed mb-8">
                    No more navigating complex menus or learning banking jargon. Simply ask questions about your finances and get instant, intelligent responses.
                </p>

                <div class="space-y-6">
                    {#each [
                        {
                            title: "Natural Language Processing",
                            description: "Ask questions in plain English and get clear, actionable insights."
                        },
                        {
                            title: "Real-time Analysis",
                            description: "Get instant analysis of your spending patterns and financial health."
                        },
                        {
                            title: "Smart Recommendations",
                            description: "Receive personalized suggestions to optimize your finances."
                        }
                    ] as item}
                        <div class="flex items-start gap-4">
                            <div class="w-1 h-1 rounded-full bg-white/20 mt-3"></div>
                            <div>
                                <div class="text-white/90 mb-1">{item.title}</div>
                                <div class="text-white/50 text-sm">{item.description}</div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</section>
<Footer />

<style>
    :global(body) {
        background-color: black;
    }
</style>
