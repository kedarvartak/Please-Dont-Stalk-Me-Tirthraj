<script lang="ts">
    import Navbar from '../../components/Navbar.svelte';
    import Footer from '../../components/Footer.svelte';
    import { fade } from 'svelte/transition';
    import { BASE_URL } from '$lib/config/api';
    import { goto } from '$app/navigation';

    let isLogin = true;
    let email = '';
    let username = '';
    let password = '';
    let error = '';
    let loading = false;

    async function handleAuth() {
        loading = true;
        error = '';
        
        try {
            const endpoint = isLogin ? '/token' : '/register';
            const body = isLogin 
                ? `username=${email}&password=${password}`
                : JSON.stringify({ email, username, password });

            const response = await fetch(`${BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': isLogin 
                        ? 'application/x-www-form-urlencoded'
                        : 'application/json',
                    'Accept': 'application/json'
                },
                credentials: 'include',  // For handling cookies if needed
                body
            });

            const data = await response.json();

            if (response.ok) {
                if (isLogin) {
                    // Store the token securely
                    localStorage.setItem('token', data.access_token);
                    // Store user data if returned
                    if (data.user) {
                        localStorage.setItem('user', JSON.stringify(data.user));
                    }
                    // Redirect to dashboard/chat
                    goto('/chat');
                } else {
                    // Registration successful
                    isLogin = true;
                    error = 'Registration successful! Please login.';
                }
            } else {
                // Handle specific error messages from backend
                error = data.detail || 'Authentication failed';
            }
        } catch (err) {
            console.error('Auth error:', err);
            error = 'An unexpected error occurred';
        } finally {
            loading = false;
        }
    }
</script>

<Navbar />

<section class="min-h-[90vh] bg-black pt-20 relative overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/[0.03] via-transparent to-transparent"></div>
    
    <div class="max-w-[400px] mx-auto px-4 sm:px-6 lg:px-8 pt-20">
        <div in:fade={{ duration: 1000 }} class="relative">
            <div class="backdrop-blur-xl bg-white/[0.02] border border-white/[0.05] rounded-2xl p-8">
                <h2 class="text-2xl text-white/90 mb-8 text-center">
                    {isLogin ? 'Welcome Back' : 'Create Account'}
                </h2>

                <form on:submit|preventDefault={handleAuth} class="space-y-6">
                    <div>
                        <label for="email" class="block text-sm text-white/40 mb-2">Email</label>
                        <input
                            type="email"
                            id="email"
                            bind:value={email}
                            class="w-full bg-white/[0.02] border border-white/[0.05] rounded-lg px-4 py-3 text-white/90 focus:outline-none focus:border-white/20"
                            required
                        />
                    </div>

                    {#if !isLogin}
                        <div>
                            <label for="username" class="block text-sm text-white/40 mb-2">Username</label>
                            <input
                                type="text"
                                id="username"
                                bind:value={username}
                                class="w-full bg-white/[0.02] border border-white/[0.05] rounded-lg px-4 py-3 text-white/90 focus:outline-none focus:border-white/20"
                                required
                            />
                        </div>
                    {/if}

                    <div>
                        <label for="password" class="block text-sm text-white/40 mb-2">Password</label>
                        <input
                            type="password"
                            id="password"
                            bind:value={password}
                            class="w-full bg-white/[0.02] border border-white/[0.05] rounded-lg px-4 py-3 text-white/90 focus:outline-none focus:border-white/20"
                            required
                        />
                    </div>

                    {#if error}
                        <div class="text-red-400 text-sm text-center">{error}</div>
                    {/if}

                    <button
                        type="submit"
                        disabled={loading}
                        class="w-full group flex items-center justify-center gap-3 text-white border border-white/10 hover:border-white/20 backdrop-blur-sm bg-white/5 hover:bg-white/10 px-8 py-4 rounded-lg font-medium transition-all duration-200 shadow-lg shadow-white/20 disabled:opacity-50"
                    >
                        {#if loading}
                            <span class="inline-block animate-spin mr-2">⟳</span>
                        {/if}
                        <span>{isLogin ? 'Sign In' : 'Create Account'}</span>
                        <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                        </svg>
                    </button>

                    <div class="text-center text-white/40 text-sm">
                        {isLogin ? "Don't have an account?" : "Already have an account?"}
                        <button
                            type="button"
                            class="text-white/90 hover:text-white ml-2"
                            on:click={() => {
                                isLogin = !isLogin;
                                error = '';
                            }}
                        >
                            {isLogin ? 'Sign Up' : 'Sign In'}
                        </button>
                    </div>
                </form>
            </div>

            <!-- Trust Indicators -->
            <div class="mt-8 flex flex-wrap justify-center items-center gap-8 text-white/40 text-sm">
                <div class="flex items-center gap-2">
                    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                    <span>Secure login</span>
                </div>
                <div class="flex items-center gap-2">
                    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <span>End-to-end encrypted</span>
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