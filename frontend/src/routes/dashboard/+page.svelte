<script>
    import Navbar from '../../components/Navbar.svelte';
    import Footer from '../../components/Footer.svelte';
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    import apiService from '$lib/services/api.js';

    let revenueChartCanvas;
    let inputMessage = '';
    let isLoading = false;
    let queryResults = null;
    let error = '';

    // Date range state
    let dateRange = 'Jan 20, 2023 - Feb 05, 2023';

    // Recent transactions
    let recentTransactions = [
        { user: 'Olivia Martin', email: 'olivia.martin@email.com', amount: '+$1,999.00' },
        { user: 'Jackson Lee', email: 'jackson.lee@email.com', amount: '+$39.00' },
        { user: 'Isabella Nguyen', email: 'isabella.nguyen@email.com', amount: '+$299.00' },
        { user: 'William Kim', email: 'will@email.com', amount: '+$99.00' },
        { user: 'Sofia Davis', email: 'sofia.davis@email.com', amount: '+$39.00' }
    ];

    async function handleQuery(event) {
        event.preventDefault();
        if (!inputMessage.trim() || isLoading) return;
        
        isLoading = true;
        error = '';

        try {
            const response = await apiService.sendChatMessage(inputMessage);
            queryResults = response;
            inputMessage = '';
        } catch (err) {
            error = err.message;
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        // Revenue Chart
        new Chart(revenueChartCanvas, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Revenue',
                    data: [3000, 1500, 2000, 4500, 4000, 2000, 3500, 4200, 4800, 3800, 2000, 1800],
                    backgroundColor: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: 6,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)',
                            drawBorder: false
                        },
                        ticks: { 
                            color: 'rgba(255, 255, 255, 0.7)',
                            font: {
                                family: "'Quicksand', sans-serif"
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: { 
                            color: 'rgba(255, 255, 255, 0.5)'
                        }
                    }
                }
            }
        });
    });
</script>

<div class="min-h-screen ">
    <Navbar />
    
    <main class="px-6 py-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-2xl font-semibold text-white">Dashboard</h1>
            <div class="flex items-center gap-4">
                <span class="text-sm text-white/60">{dateRange}</span>
                <button class="px-3 py-1.5 text-sm text-white/90 bg-white/10 rounded-md hover:bg-white/20 transition-colors">
                    Download
                </button>
            </div>
        </div>

        <!-- Navigation -->
        <div class="flex gap-6 mb-8 border-b border-white/10">
            <button class="px-4 py-2 text-sm text-white/90 border-b-2 border-white -mb-[2px]">Overview</button>
            <button class="px-4 py-2 text-sm text-white/60 hover:text-white/90">Analytics</button>
            <button class="px-4 py-2 text-sm text-white/60 hover:text-white/90">Reports</button>
            <button class="px-4 py-2 text-sm text-white/60 hover:text-white/90">Notifications</button>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <div class="flex justify-between items-start mb-4">
                    <div class="text-sm text-white/40">Total Revenue</div>
                    <div class="text-xs text-green-400">+20.1% from last month</div>
                </div>
                <div class="text-2xl font-semibold text-white mb-1">$45,231.89</div>
            </div>

            <div class="p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <div class="flex justify-between items-start mb-4">
                    <div class="text-sm text-white/40">Subscriptions</div>
                    <div class="text-xs text-green-400">+180.1% from last month</div>
                </div>
                <div class="text-2xl font-semibold text-white mb-1">+2,350</div>
            </div>

            <div class="p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <div class="flex justify-between items-start mb-4">
                    <div class="text-sm text-white/40">Sales</div>
                    <div class="text-xs text-green-400">+19% from last month</div>
                </div>
                <div class="text-2xl font-semibold text-white mb-1">+12,234</div>
            </div>

            <div class="p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <div class="flex justify-between items-start mb-4">
                    <div class="text-sm text-white/40">Active Now</div>
                    <div class="text-xs text-green-400">+201 since last hour</div>
                </div>
                <div class="text-2xl font-semibold text-white mb-1">+573</div>
            </div>
        </div>

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Chart Section -->
            <div class="lg:col-span-2 p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <h3 class="text-lg text-white mb-6">Overview</h3>
                <div class="h-[300px]">
                    <canvas bind:this={revenueChartCanvas}></canvas>
                </div>
            </div>

            <!-- Recent Sales -->
            <div class="p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                <h3 class="text-lg text-white mb-4">Recent Sales</h3>
                <p class="text-sm text-white/60 mb-6">You made 265 sales this month.</p>
                
                <div class="space-y-6">
                    {#each recentTransactions as transaction}
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="w-8 h-8 rounded-full bg-white/10"></div>
                                <div>
                                    <div class="text-sm font-medium text-white">{transaction.user}</div>
                                    <div class="text-xs text-white/60">{transaction.email}</div>
                                </div>
                            </div>
                            <div class="text-sm text-white">{transaction.amount}</div>
                        </div>
                    {/each}
                </div>
            </div>
        </div>

        <!-- NLP Query Interface -->
        <div class="mt-8 p-6 rounded-xl bg-white/[0.02] border border-white/[0.05]">
            <div class="max-w-3xl mx-auto">
                <form on:submit|preventDefault={handleQuery} class="relative">
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
                        {isLoading ? 'Processing...' : 'Ask'}
                    </button>
                </form>

                {#if queryResults}
                    <div class="mt-6 space-y-4">
                        <div class="text-white/60 text-sm">{queryResults.explanation}</div>
                        {#if queryResults.results?.length}
                            <div class="overflow-x-auto">
                                <table class="w-full">
                                    <thead>
                                        <tr>
                                            {#each Object.keys(queryResults.results[0]) as header}
                                                <th class="text-left p-2 text-white/40 text-xs uppercase border-b border-white/[0.05]">
                                                    {header}
                                                </th>
                                            {/each}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each queryResults.results as row}
                                            <tr class="border-b border-white/[0.03]">
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
    </main>

    <Footer />
</div>

<style>
    :global(body) {
        background-color: black;
    }
</style>