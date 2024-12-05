<script>
    import { authStore } from '$lib/stores/authStore';
    import { goto } from '$app/navigation';
    import { fade } from 'svelte/transition';
    
    let isMenuOpen = false;
    let isProfileOpen = false;

    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
    }

    function toggleProfile() {
        isProfileOpen = !isProfileOpen;
    }

    async function handleLogout() {
        localStorage.removeItem('token');
        localStorage.removeItem('userEmail');
        authStore.set({
            isLoggedIn: false,
            userEmail: null,
            username: null,
            token: null
        });
        isProfileOpen = false;
        goto('/');
    }
</script>

<nav class="fixed top-0 left-0 right-0 z-50">
    <div class="backdrop-blur-xl bg-black/40 border-b border-white/10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <a href="/" class="group">
                        <span class="text-2xl font-bold bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent group-hover:to-white/90 transition-all duration-300">FINN</span>
                    </a>
                </div>

                <!-- Desktop Navigation -->
                <div class="hidden md:flex md:items-center md:space-x-8">
                    <a href="/dashboard" class="nav-link group relative">
                        <span class="absolute inset-x-0 -bottom-[1.5px] h-[1.5px] bg-white/80 scale-x-0 group-hover:scale-x-100 transition-transform duration-200 origin-left"></span>
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                        </svg>
                        Dashboard
                    </a>
                    <a href="/analytics" class="nav-link group relative">
                        <span class="absolute inset-x-0 -bottom-[1.5px] h-[1.5px] bg-white/80 scale-x-0 group-hover:scale-x-100 transition-transform duration-200 origin-left"></span>
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        Analytics
                    </a>
                    <a href="/transactions" class="nav-link group relative">
                        <span class="absolute inset-x-0 -bottom-[1.5px] h-[1.5px] bg-white/80 scale-x-0 group-hover:scale-x-100 transition-transform duration-200 origin-left"></span>
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Transactions
                    </a>
                    <a href="/chat" class="nav-link group relative">
                        <span class="absolute inset-x-0 -bottom-[1.5px] h-[1.5px] bg-white/80 scale-x-0 group-hover:scale-x-100 transition-transform duration-200 origin-left"></span>
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Insights
                    </a>
                </div>

                <!-- Auth Buttons / Profile -->
                <div class="hidden md:flex items-center space-x-4">
                    {#if !$authStore.isLoggedIn}
                        <a href="/auth" class="px-4 py-2 text-sm font-medium text-white/80 hover:text-white transition-colors">
                            Sign in
                        </a>
                        <a href="/auth" class="px-4 py-2 text-sm font-medium text-black bg-white hover:bg-white/90 rounded-lg transition-colors">
                            Get Started
                        </a>
                    {:else}
                        <div class="relative">
                            <button 
                                on:click={toggleProfile}
                                class="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-white/[0.05] transition-colors"
                            >
                                <div class="w-8 h-8 rounded-full bg-white/[0.05] flex items-center justify-center">
                                    <svg class="w-4 h-4 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <span class="text-sm font-medium text-white/80">{$authStore.username || 'User'}</span>
                            </button>

                            {#if isProfileOpen}
                                <div 
                                    class="absolute right-0 mt-2 w-56 rounded-xl overflow-hidden border border-white/[0.05] backdrop-blur-xl"
                                    in:fade={{ duration: 100 }}
                                    out:fade={{ duration: 100 }}
                                >
                                    <div class="bg-black/90">
                                        <a 
                                            href="/settings" 
                                            class="flex items-center px-4 py-3 text-sm text-white/80 hover:bg-white/[0.05] transition-colors"
                                        >
                                            <svg class="w-4 h-4 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                            Settings
                                        </a>
                                        <button
                                            on:click={handleLogout}
                                            class="flex items-center w-full px-4 py-3 text-sm text-white/80 hover:bg-white/[0.05] transition-colors"
                                        >
                                            <svg class="w-4 h-4 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                            </svg>
                                            Sign out
                                        </button>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>

                <!-- Mobile menu button -->
                <div class="md:hidden">
                    <button 
                        on:click={toggleMenu}
                        class="inline-flex items-center justify-center p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/[0.05] transition-colors"
                    >
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            {#if isMenuOpen}
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
                            {:else}
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
                            {/if}
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Navigation -->
        {#if isMenuOpen}
            <div class="md:hidden border-t border-white/[0.05]" transition:fade={{ duration: 200 }}>
                <div class="px-2 pt-2 pb-3 space-y-1">
                    <a href="/dashboard" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                        </svg>
                        Dashboard
                    </a>
                    <a href="/analytics" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        Analytics
                    </a>
                    <a href="/transactions" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Transactions
                    </a>
                    <a href="/insights" class="mobile-nav-link">
                        <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Insights
                    </a>

                    {#if $authStore.isLoggedIn}
                        <div class="pt-4 mt-4 border-t border-white/[0.05]">
                            <div class="px-4 py-2 text-sm text-white/60">
                                {$authStore.username || 'User'}
                            </div>
                            <a 
                                href="/settings" 
                                class="mobile-nav-link"
                            >
                                <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                Settings
                            </a>
                            <button
                                on:click={handleLogout}
                                class="mobile-nav-link w-full text-left"
                            >
                                <svg class="w-5 h-5 mr-3 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                </svg>
                                Sign out
                            </button>
                        </div>
                    {:else}
                        <div class="pt-4 mt-4 border-t border-white/[0.05] px-4 space-y-3">
                            <a href="/auth" class="block px-4 py-2 text-sm font-medium text-white/80 hover:text-white transition-colors">
                                Sign in
                            </a>
                            <a href="/auth" class="block px-4 py-2 text-sm font-medium text-black bg-white hover:bg-white/90 rounded-lg text-center transition-colors">
                                Get Started
                            </a>
                        </div>
                    {/if}
                </div>
            </div>
        {/if}
    </div>
</nav>

<style>
    .nav-link {
        @apply flex items-center text-white/80 hover:text-white text-sm font-medium transition-colors;
    }

    .mobile-nav-link {
        @apply flex items-center px-4 py-3 text-white/80 hover:text-white hover:bg-white/[0.05] rounded-lg transition-colors;
    }
</style> 