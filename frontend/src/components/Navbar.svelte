<script>
    import { authStore } from '$lib/stores/authStore';
    import { goto } from '$app/navigation';
    
    let isMenuOpen = false;
    let isProfileOpen = false;

    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
    }

    function toggleProfile() {
        isProfileOpen = !isProfileOpen;
    }

    async function handleLogout() {
        // Clear local storage
        localStorage.removeItem('token');
        localStorage.removeItem('userEmail');
        
        // Update auth store
        authStore.set({
            isLoggedIn: false,
            userEmail: null,
            token: null
        });

        // Close profile dropdown
        isProfileOpen = false;
        
        // Redirect to home page
        goto('/');
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
                            {#if !$authStore.isLoggedIn}
                                <button class="px-4 py-2 text-[15px] font-medium text-white/90 hover:text-white transition-colors">
                                    Sign in
                                </button>
                                <button class="bg-gradient-to-r bg-white text-black px-4 py-2 rounded-md text-[15px] font-medium transition-all duration-200 shadow-lg shadow-purple-500/20">
                                    Get Started
                                </button>
                            {:else}
                                <div class="relative">
                                    <button 
                                        on:click={toggleProfile}
                                        class="flex items-center justify-center w-10 h-10 rounded-lg bg-white/[0.02] hover:bg-white/[0.05] border border-white/[0.05] text-white/90 hover:text-white transition-all duration-200"
                                    >
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                    </button>

                                    {#if isProfileOpen}
                                        <div 
                                            class="absolute right-0 mt-2 w-56 rounded-xl overflow-hidden shadow-lg border border-white/[0.05] backdrop-blur-xl"
                                            in:fade={{ duration: 100 }}
                                        >
                                            <div class="bg-black/90">
                                                <!-- Profile Header -->
                                                <div class="px-4 py-3 border-b border-white/[0.05]">
                                                    <div class="text-sm font-medium text-white/90">Account</div>
                                                    <div class="text-sm text-white/60 truncate">
                                                        {$authStore.userEmail}
                                                    </div>
                                                </div>
                                                
                                                <!-- Menu Items -->
                                                <div class="py-1">
                                                    <a 
                                                        href="/settings" 
                                                        class="flex items-center px-4 py-2 text-sm text-white/80 hover:text-white hover:bg-white/[0.02] transition-colors"
                                                    >
                                                        <svg class="w-4 h-4 mr-2 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                        </svg>
                                                        Settings
                                                    </a>
                                                    <button
                                                        on:click={handleLogout}
                                                        class="flex items-center w-full px-4 py-2 text-sm text-white/80 hover:text-white hover:bg-white/[0.02] transition-colors"
                                                    >
                                                        <svg class="w-4 h-4 mr-2 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                                        </svg>
                                                        Sign out
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    {/if}
                                </div>
                            {/if}
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
                        {#if !$authStore.isLoggedIn}
                        <button 
                            on:click={() => goto('/auth')}
                            class="px-4 py-2 text-[15px] font-medium text-white/90 hover:text-white transition-colors"
                        >
                            Sign in
                        </button>
                        <button 
                            on:click={() => goto('/auth')}
                            class="bg-gradient-to-r bg-white text-black px-4 py-2 rounded-md text-[15px] font-medium transition-all duration-200 shadow-lg shadow-purple-500/20"
                        >
                            Get Started
                        </button>
                    {:else}
                            <div class="px-4 py-2 text-sm text-white/70">
                                {$authStore.userEmail}
                            </div>
                            <button
                                on:click={handleLogout}
                                class="w-full text-left px-4 py-2 text-sm text-white/90 hover:text-white hover:bg-white/10"
                            >
                                Log out
                            </button>
                        {/if}
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