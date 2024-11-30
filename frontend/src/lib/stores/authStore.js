import { writable } from 'svelte/store';

export const authStore = writable({
    isLoggedIn: false,
    userEmail: null,
    token: null
});

// Initialize store from localStorage on app load
if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    const userEmail = localStorage.getItem('userEmail');
    if (token && userEmail) {
        authStore.set({
            isLoggedIn: true,
            userEmail: userEmail,
            token: token
        });
    }
}