<script>
    let isMenuOpen = false;

    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
    }
</script>

<nav class="fixed top-0 left-0 right-0 z-50">
    <div class="backdrop-blur-xl bg-black/40 border-b border-white/10 shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo and Brand -->
                <div class="flex items-center">
                    <a href="/" class="flex items-center group">
                        <span class="text-2xl font-semibold text-white group-hover:text-white/90 transition-colors">FINN</span>
                    </a>
                </div>

                <!-- Desktop Navigation -->
                <div class="hidden md:block">
                    <div class="flex items-center space-x-6">
                        <a href="/analytics" class="nav-link group">
                            <svg class="w-4 h-4 mr-2 opacity-80 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            Analytics
                        </a>
                        <a href="/transactions" class="nav-link group">
                            <svg class="w-4 h-4 mr-2 opacity-80 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Transactions
                        </a>
                        <a href="/insights" class="nav-link group">
                            <svg class="w-4 h-4 mr-2 opacity-80 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Insights
                        </a>
                        <div class="flex items-center space-x-3 ml-6 pl-6 border-l border-white/10">
                            <button class="px-4 py-2 text-[15px] font-medium text-white/90 hover:text-white transition-colors">
                                Sign in
                            </button>
                            <button class="bg-gradient-to-r bg-white text-black px-4 py-2 rounded-md text-[15px] font-medium transition-all duration-200 shadow-lg shadow-purple-500/20">
                                Get Started
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Mobile menu button -->
                <div class="md:hidden">
                    <button 
                        on:click={toggleMenu}
                        class="text-white/80 hover:text-white p-2 rounded-lg transition-colors"
                    >
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            {#if isMenuOpen}
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            {:else}
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                            {/if}
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Navigation -->
        {#if isMenuOpen}
            <div class="md:hidden bg-black/40 backdrop-blur-xl border-t border-white/5">
                <div class="px-2 pt-2 pb-3 space-y-1">
                    <a href="/analytics" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        Analytics
                    </a>
                    <a href="/transactions" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Transactions
                    </a>
                    <a href="/insights" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Insights
                    </a>
                    <div class="pt-4 mt-4 border-t border-white/10">
                        <button class="w-full text-center text-white/90 hover:text-white px-4 py-2 rounded-md text-lg font-medium transition-colors mb-2">
                            Sign in
                        </button>
                        <button class="w-full text-center bg-gradient-to-r bg-white text-black px-4 py-2 rounded-md text-[15px] font-medium transition-all duration-200 shadow-lg shadow-purple-500/20">
                            Get Started
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</nav>

<style>
    .nav-link {
        @apply flex items-center text-white/80 hover:text-white px-3 py-2 rounded-md text-[15px] font-medium transition-colors;
    }

    .mobile-nav-link {
        @apply flex items-center text-white/80 hover:text-white px-3 py-3 rounded-md text-lg font-medium transition-colors;
    }
</style> 