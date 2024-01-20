import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		greetings: 'Hello'
	}
});

export default app;