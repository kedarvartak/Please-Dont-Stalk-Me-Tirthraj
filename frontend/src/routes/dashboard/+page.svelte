<script>
    import Navbar from '../../components/Navbar.svelte';
    import Footer from '../../components/Footer.svelte';
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    import apiService from '$lib/services/api.js';
    import { tweened } from 'svelte/motion';
    import { cubicOut } from 'svelte/easing';
    import { browser } from '$app/environment';

    let revenueChart;
    let revenueChartCanvas;
    let inputMessage = '';
    let isLoading = false;
    let queryResults = null;
    let error = '';

    // Date range state
    let dateRange = new Date().toLocaleDateString('en-US', { 
        year: 'numeric',
        month: 'long'
    });

    // Recent transactions - Updated with financial transactions
    let recentTransactions = [
        { 
            merchant: 'Whole Foods Market',
            category: 'Groceries',
            date: '2024-03-15',
            amount: '-$156.32'
        },
        { 
            merchant: 'Netflix',
            category: 'Entertainment',
            date: '2024-03-14',
            amount: '-$15.99'
        },
        { 
            merchant: 'Salary Deposit',
            category: 'Income',
            date: '2024-03-10',
            amount: '+$3,450.00'
        },
        { 
            merchant: 'Amazon',
            category: 'Shopping',
            date: '2024-03-08',
            amount: '-$67.99'
        },
        { 
            merchant: 'Uber',
            category: 'Transportation',
            date: '2024-03-07',
            amount: '-$24.50'
        }
    ];

    // Add state for active tab
    let activeTab = 'overview';

    // Sample analytics data
    let spendingTrends = {
        categories: {
            groceries: { current: 650, previous: 580, change: 12.1 },
            entertainment: { current: 180, previous: 220, change: -18.2 },
            transportation: { current: 200, previous: 180, change: 11.1 },
            utilities: { current: 320, previous: 310, change: 3.2 },
            shopping: { current: 450, previous: 600, change: -25.0 },
            dining: { current: 380, previous: 290, change: 31.0 }
        },
        topMerchants: [
            { name: 'Whole Foods', amount: 420, transactions: 5 },
            { name: 'Amazon', amount: 350, transactions: 8 },
            { name: 'Netflix', amount: 45, transactions: 3 },
            { name: 'Uber', amount: 120, transactions: 6 }
        ],
        insights: [
            { type: 'alert', message: 'Dining expenses increased by 31% this month' },
            { type: 'success', message: 'Shopping expenses reduced by 25%' },
            { type: 'info', message: 'Your grocery spending is higher than 80% of users' }
        ]
    };

    let monthlyTrendCanvas;
    let categoryDistCanvas;
    let savingsProgressCanvas;

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

    function initializeOverviewChart() {
        if (!revenueChartCanvas) return;

        // Destroy the existing chart instance if it exists
        if (revenueChart) {
            revenueChart.destroy();
        }

        // Create a new chart instance
        revenueChart = new Chart(revenueChartCanvas, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Revenue',
                    data: [4500, 4800, 5000, 5200, 5400, 5600],
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                }
            }
        });
    }

    // Watch for tab changes to reinitialize charts
    $: if (activeTab === 'overview' && browser) {
        setTimeout(() => {
            initializeOverviewChart();
        }, 100); // Small delay to ensure canvas elements are mounted
    }

    $: if (activeTab === 'analytics' && browser) {
        setTimeout(() => {
            initializeAnalyticsCharts();
        }, 100);
    }

    $: if (activeTab === 'overview' && browser) {
        setTimeout(() => {
            // Reinitialize charts when tab changes
            if (browser) {
                const event = new Event('resize');
                window.dispatchEvent(event);
            }
        }, 0);
    }

    // Progress bar animation
    function createProgressBar(value) {
        return tweened(0, {
            duration: 1000,
            easing: cubicOut
        }).set(value);
    }

    // Function to initialize analytics charts
    function initializeAnalyticsCharts() {
        if (!monthlyTrendCanvas || !categoryDistCanvas || !savingsProgressCanvas) return;

        // Monthly Spending Trend Chart
        new Chart(monthlyTrendCanvas, {
            type: 'line',
            data: {
                labels: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
                datasets: [{
                    label: 'Spending',
                    data: [2800, 3200, 3800, 2900, 3100, 2800],
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Average',
                    data: [3000, 3000, 3000, 3000, 3000, 3000],
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                }
            }
        });

        // Category Distribution Chart
        new Chart(categoryDistCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Groceries', 'Entertainment', 'Transportation', 'Utilities', 'Shopping', 'Dining'],
                datasets: [{
                    data: [650, 180, 200, 320, 450, 380],
                    backgroundColor: [
                        'rgba(255, 255, 255, 0.8)',
                        'rgba(255, 255, 255, 0.7)',
                        'rgba(255, 255, 255, 0.6)',
                        'rgba(255, 255, 255, 0.5)',
                        'rgba(255, 255, 255, 0.4)',
                        'rgba(255, 255, 255, 0.3)'
                    ],
                    borderColor: 'rgba(0, 0, 0, 0.1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)',
                            padding: 20
                        }
                    }
                }
            }
        });

        // Savings Progress Chart
        new Chart(savingsProgressCanvas, {
            type: 'bar',
            data: {
                labels: ['Emergency Fund', 'Vacation', 'New Car'],
                datasets: [{
                    label: 'Current',
                    data: [8000, 2500, 15000],
                    backgroundColor: 'rgba(255, 255, 255, 0.3)'
                },
                {
                    label: 'Goal',
                    data: [10000, 5000, 30000],
                    backgroundColor: 'rgba(255, 255, 255, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.7)'
                        }
                    }
                }
            }
        });
    }

    function downloadCSV() {
        // Placeholder function for CSV download
        console.log("Downloading CSV...");
    }

    function downloadPDF() {
        // Placeholder function for PDF download
        console.log("Downloading PDF...");
    }

    // Sample AI-generated insights
    let aiInsights = [
        { title: 'Spending Alert', message: 'Your dining expenses are 20% higher than last month.' },
        { title: 'Savings Opportunity', message: 'Reducing entertainment expenses by 10% could save you $50 monthly.' },
        { title: 'Budget Recommendation', message: 'Consider setting a monthly budget of $300 for groceries.' }
    ];
</script>

<div class="min-h-screen bg-black">
    <Navbar />
    
    <main class="px-4 py-8 md:px-6 lg:px-8 mt-12 relative">
        <!-- Background gradient -->
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/[0.03] via-transparent to-transparent pointer-events-none"></div>

        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 relative">
            <h1 class="text-2xl font-semibold text-white/90 mb-4 md:mb-0">Dashboard</h1>
            <div class="flex items-center gap-4">
                <span class="text-sm text-white/60">{dateRange}</span>
                <button class="px-3 py-1.5 text-sm text-white/80 backdrop-blur-sm bg-white/[0.05] border border-white/[0.05] rounded-md hover:bg-white/[0.08] transition-all">
                    Download
                </button>
            </div>
        </div>

        <!-- Navigation -->
        <div class="flex gap-4 md:gap-6 mb-8 border-b border-white/[0.05] overflow-x-auto">
            <button 
                class="px-4 py-2 text-sm {activeTab === 'overview' ? 'text-white/90 border-b-2 border-white/80' : 'text-white/40 hover:text-white/60'} transition-colors"
                on:click={() => activeTab = 'overview'}
            >
                Overview
            </button>
            <button 
                class="px-4 py-2 text-sm {activeTab === 'analytics' ? 'text-white/90 border-b-2 border-white/80' : 'text-white/40 hover:text-white/60'} transition-colors"
                on:click={() => activeTab = 'analytics'}
            >
                Analytics
            </button>
            <button 
                class="px-4 py-2 text-sm {activeTab === 'reports' ? 'text-white/90 border-b-2 border-white/80' : 'text-white/40 hover:text-white/60'} transition-colors"
                on:click={() => activeTab = 'reports'}
            >
                AI Reports
            </button>
            
        </div>

        <!-- Conditional Content Section -->
        {#if activeTab === 'overview'}
            <!-- Stats Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {#each [
                    { label: 'Monthly Income', value: '$4,500.00', change: '+5.2%', positive: true },
                    { label: 'Monthly Expenses', value: '$2,800.00', change: '+12.3%', positive: false },
                    { label: 'Savings Rate', value: '26.7%', change: '+2.5%', positive: true },
                    { label: 'Investment Returns', value: '+$1,234.56', change: '+8.3%', positive: true }
                ] as stat}
                    <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05] hover:bg-white/[0.04] transition-all">
                        <div class="flex justify-between items-start mb-4">
                            <div class="text-sm text-white/40">{stat.label}</div>
                            <div class="text-xs {stat.positive ? 'text-white/80' : 'text-white/60'}">{stat.change} from last month</div>
                        </div>
                        <div class="text-2xl font-semibold text-white/90 mb-1">{stat.value}</div>
                    </div>
                {/each}
            </div>

            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Chart Section -->
                <div class="lg:col-span-2 p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05] hover:bg-white/[0.04] transition-all">
                    <h3 class="text-lg text-white/90 mb-6">Overview</h3>
                    <div class="h-[300px]">
                        <canvas bind:this={revenueChartCanvas}></canvas>
                    </div>
                </div>

                <!-- Recent Transactions -->
                <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                    <h3 class="text-lg text-white/90 mb-4">Recent Transactions</h3>
                    <div class="space-y-4">
                        {#each recentTransactions as transaction}
                            <div class="flex items-center justify-between p-3 rounded-lg bg-white/[0.02] border border-white/[0.02] hover:bg-white/[0.04] transition-all">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-full bg-white/[0.03] border border-white/[0.05] flex items-center justify-center">
                                        <span class="text-white/60 text-xs">{transaction.category[0]}</span>
                                    </div>
                                    <div>
                                        <div class="text-sm font-medium text-white/90">{transaction.merchant}</div>
                                        <div class="text-xs text-white/40">{transaction.category} • {new Date(transaction.date).toLocaleDateString()}</div>
                                    </div>
                                </div>
                                <div class="text-sm {transaction.amount.startsWith('+') ? 'text-white/90' : 'text-white/70'}">{transaction.amount}</div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        {:else if activeTab === 'analytics'}
            <div class="space-y-6">
                <!-- Spending Insights -->
                <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                    <h3 class="text-lg text-white/90 mb-4">Key Insights</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {#each spendingTrends.insights as insight}
                            <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                                <div class="flex items-start gap-3">
                                    <div class="w-8 h-8 rounded-full bg-white/[0.05] flex items-center justify-center">
                                        {#if insight.type === 'alert'}
                                            <span class="text-white/60">⚠️</span>
                                        {:else if insight.type === 'success'}
                                            <span class="text-white/60">✓</span>
                                        {:else}
                                            <span class="text-white/60">ℹ️</span>
                                        {/if}
                                    </div>
                                    <p class="text-sm text-white/80">{insight.message}</p>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Spending Trends -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Monthly Spending Trend -->
                    <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="text-lg text-white/90">Monthly Spending Trend</h3>
                            <select class="bg-white/[0.05] border border-white/[0.05] rounded-lg px-3 py-1.5 text-sm text-white/80">
                                <option value="6">Last 6 months</option>
                                <option value="12">Last 12 months</option>
                            </select>
                        </div>
                        <div class="h-[300px]">
                            <canvas bind:this={monthlyTrendCanvas}></canvas>
                        </div>
                    </div>

                    <!-- Category Distribution -->
                    <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                        <h3 class="text-lg text-white/90 mb-6">Category Distribution</h3>
                        <div class="h-[300px]">
                            <canvas bind:this={categoryDistCanvas}></canvas>
                        </div>
                    </div>
                </div>

                <!-- Predictive Analysis -->
                <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                    <h3 class="text-lg text-white/90 mb-6">Spending Forecast</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                            <div class="text-sm text-white/60 mb-2">Predicted Next Month</div>
                            <div class="text-2xl text-white/90 mb-1">$3,240</div>
                            <div class="text-xs text-white/40">Based on current trends</div>
                        </div>
                        <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                            <div class="text-sm text-white/60 mb-2">Suggested Budget</div>
                            <div class="text-2xl text-white/90 mb-1">$2,800</div>
                            <div class="text-xs text-white/40">15% reduction recommended</div>
                        </div>
                        <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                            <div class="text-sm text-white/60 mb-2">Potential Savings</div>
                            <div class="text-2xl text-white/90 mb-1">$440</div>
                            <div class="text-xs text-white/40">If budget is followed</div>
                        </div>
                    </div>
                </div>

                <!-- Spending Patterns -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Category Comparison -->
                    <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                        <h3 class="text-lg text-white/90 mb-6">Category Comparison</h3>
                        <div class="space-y-4">
                            {#each Object.entries(spendingTrends.categories) as [category, data]}
                                <div class="space-y-2">
                                    <div class="flex justify-between items-center">
                                        <span class="text-sm text-white/80 capitalize">{category}</span>
                                        <div class="flex items-center gap-3">
                                            <div class="text-xs text-white/40">Previous: ${data.previous}</div>
                                            <div class="text-sm text-white/90">Current: ${data.current}</div>
                                            <div class="text-xs {data.change >= 0 ? 'text-white/80' : 'text-white/60'}">
                                                {data.change >= 0 ? '+' : ''}{data.change}%
                                            </div>
                                        </div>
                                    </div>
                                    <div class="relative h-2">
                                        <div class="absolute inset-0 rounded-full bg-white/[0.03]"></div>
                                        <div class="absolute inset-0 rounded-full bg-white/[0.15]"
                                             style="width: {(data.previous / 1000) * 100}%"></div>
                                        <div class="absolute inset-0 rounded-full bg-white/[0.3]"
                                             style="width: {(data.current / 1000) * 100}%"></div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>

                    <!-- Spending Anomalies -->
                    <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                        <h3 class="text-lg text-white/90 mb-6">Unusual Spending Patterns</h3>
                        <div class="space-y-4">
                            <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 rounded-full bg-white/[0.05] flex items-center justify-center">
                                        <span class="text-white/60">⚠️</span>
                                    </div>
                                    <div class="text-sm text-white/90">Higher than usual dining expenses</div>
                                </div>
                                <div class="text-xs text-white/40">31% increase from your 6-month average</div>
                            </div>
                            <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 rounded-full bg-white/[0.05] flex items-center justify-center">
                                        <span class="text-white/60">✓</span>
                                    </div>
                                    <div class="text-sm text-white/90">Lower shopping expenses</div>
                                </div>
                                <div class="text-xs text-white/40">25% decrease from your typical spending</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Savings Goals Progress -->
                <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                    <h3 class="text-lg text-white/90 mb-6">Savings Goals Progress</h3>
                    <div class="h-[300px]">
                        <canvas bind:this={savingsProgressCanvas}></canvas>
                    </div>
                </div>
            </div>
        {:else if activeTab === 'reports'}
            <!-- AI Reports Content -->
            <div class="space-y-6">
                <!-- AI-Generated Insights -->
                <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                    <h3 class="text-lg text-white/90 mb-4">AI-Generated Insights</h3>
                    <div class="space-y-4">
                        {#each aiInsights as insight}
                            <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05]">
                                <h4 class="text-md text-white/80 mb-2">{insight.title}</h4>
                                <p class="text-sm text-white/70">{insight.message}</p>
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Download Options -->
                <div class="p-6 rounded-xl backdrop-blur-md bg-white/[0.02] border border-white/[0.05]">
                    <h3 class="text-lg text-white/90 mb-4">Download Reports</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05] flex flex-col items-center justify-center">
                            <h4 class="text-md text-white/80 mb-2">CSV Format</h4>
                            <button 
                                class="px-4 py-2 text-sm text-white/80 backdrop-blur-sm bg-white/[0.05] border border-white/[0.05] rounded-md hover:bg-white/[0.08] transition-all"
                                on:click={downloadCSV}
                            >
                                Download CSV
                            </button>
                        </div>
                        <div class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.05] flex flex-col items-center justify-center">
                            <h4 class="text-md text-white/80 mb-2">PDF Format</h4>
                            <button 
                                class="px-4 py-2 text-sm text-white/80 backdrop-blur-sm bg-white/[0.05] border border-white/[0.05] rounded-md hover:bg-white/[0.08] transition-all"
                                on:click={downloadPDF}
                            >
                                Download PDF
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        {/if}

       
       
    </main>

    <Footer />
</div>

<style>
    :global(body) {
        background-color: black;
    }
</style>