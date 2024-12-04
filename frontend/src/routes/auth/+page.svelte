<script lang="ts">
    import Navbar from '../../components/Navbar.svelte';
    import Footer from '../../components/Footer.svelte';
    import { fade } from 'svelte/transition';
    import { BASE_URL } from '$lib/config/api';
    import { goto } from '$app/navigation';
    import { authStore } from '$lib/stores/authStore';

    let isLogin = true;
    let email = '';
    let username = '';
    let password = '';
    let verificationCode = '';
    let showVerification = false;
    let error = '';
    let loading = false;

    async function handleAuth() {
        loading = true;
        error = '';
        
        try {
            if (isLogin) {
                const endpoint = '/token';
                const body = `username=${email}&password=${password}`;

                const response = await fetch(`${BASE_URL}${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/json'
                    },
                    credentials: 'include',  // For handling cookies if needed
                    body
                });

                const data = await response.json();

                if (response.ok) {
                    // Store the token securely
                    localStorage.setItem('token', data.access_token);
                    // Store user data if returned
                    if (data.user) {
                        localStorage.setItem('user', JSON.stringify(data.user));
                    }
                    // Store user data
                    localStorage.setItem('userEmail', email);
                    authStore.set({
                        isLoggedIn: true,
                        userEmail: email,
                        token: data.access_token
                    });
                    // Redirect to dashboard/chat
                    goto('/');
                } else {
                    // Handle specific error messages from backend
                    error = data.detail || 'Authentication failed';
                }
            } else {
                // Registration with verification
                const registerResponse = await fetch(`${BASE_URL}/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, username, password })
                });

                const data = await registerResponse.json();

                if (registerResponse.ok) {
                    showVerification = true;
                } else {
                    error = data.detail || 'Registration failed';
                }
            }
        } catch (err) {
            console.error('Auth error:', err);
            error = 'An unexpected error occurred';
        } finally {
            loading = false;
        }
    }

    async function handleVerification() {
        loading = true;
        error = '';

        try {
            const response = await fetch(`${BASE_URL}/verify-email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    email, 
                    code: verificationCode 
                })
            });

            const data = await response.json();

            if (response.ok) {
                isLogin = true;
                showVerification = false;
                error = 'Email verified! Please login.';
            } else {
                error = data.detail || 'Verification failed';
            }
        } catch (err) {
            console.error('Verification error:', err);
            error = 'An unexpected error occurred';
        } finally {
            loading = false;
        }
    }

    async function handleResendCode() {
        loading = true;
        error = '';

        try {
            const response = await fetch(`${BASE_URL}/resend-verification`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (response.ok) {
                error = 'New verification code sent!';
            } else {
                error = data.detail || 'Failed to resend code';
            }
        } catch (err) {
            console.error('Resend error:', err);
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
                    {#if showVerification}
                        Verify Your Email
                    {:else}
                        {isLogin ? 'Welcome Back' : 'Create Account'}
                    {/if}
                </h2>

                {#if error}
                    <div class="bg-green-300 border border-red-500/20 rounded-lg p-3 mb-4">
                        <p class="text-white text-sm">{error}</p>
                    </div>
                {/if}

                {#if showVerification}
                    <div class="bg-white/[0.02] backdrop-blur-xl border border-white/[0.05] p-8 rounded-2xl">
                        <div class="space-y-6">
                            <div class="text-center">
                                <h3 class="text-xl text-white/90 mb-2">Check Your Email</h3>
                                <p class="text-white/60 text-sm">
                                    We've sent a verification code to your email
                                </p>
                            </div>

                            <form on:submit|preventDefault={handleVerification} class="space-y-6">
                                <div>
                                    <label for="verificationCode" class="block text-sm text-white/40 mb-2">Verification Code</label>
                                    <div class="relative">
                                        <input
                                            type="text"
                                            id="verificationCode"
                                            bind:value={verificationCode}
                                            class="w-full bg-white/[0.02] border border-white/[0.05] rounded-lg px-4 py-3 text-white/90 focus:outline-none focus:border-white/20"
                                            placeholder="Enter 6-digit code"
                                            required
                                        />
                                        <svg class="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                                        </svg>
                                    </div>
                                </div>

                                <button
                                    type="submit"
                                    disabled={loading}
                                    class="w-full group flex items-center justify-center gap-3 text-white border border-white/10 hover:border-white/20 backdrop-blur-sm bg-white/5 hover:bg-white/10 px-8 py-4 rounded-lg font-medium transition-all duration-200 shadow-lg shadow-white/20 disabled:opacity-50"
                                >
                                    {#if loading}
                                        <span class="inline-block animate-spin mr-2">⟳</span>
                                    {/if}
                                    <span>Verify Email</span>
                                    <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                                    </svg>
                                </button>

                                <div class="text-center text-white/40 text-sm">
                                    Didn't receive the code?
                                    <button
                                        type="button"
                                        class="text-white/90 hover:text-white ml-2 transition-colors"
                                        on:click={handleResendCode}
                                    >
                                        Resend Code
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                {:else}
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
                {/if}
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