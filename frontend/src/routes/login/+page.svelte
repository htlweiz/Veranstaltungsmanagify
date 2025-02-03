<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Eye, EyeOff, RefreshCw, House } from 'lucide-svelte';
	import { PUBLIC_AUTH_URL } from '$env/static/public';
	import MicrosoftLogo from '$lib/Microsoft_logo.svelte';
	import Label from '$lib/components/ui/label/label.svelte';

	let loading = false;
	let passVisible = false;

	let username = '';
	let password = '';

	async function login() {
		loading = true;
		const res = await fetch(PUBLIC_AUTH_URL + '/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: username, password: password })
		});
		if (res.status === 200) {
			window.location.href = '/';
		} else {
			loading = false;
			alert('Invalid credentials');
		}
	}
</script>

<Button
	class="absolute left-2 top-2 z-50 aspect-square rounded-lg bg-slate-800/50 p-1 outline outline-2 outline-slate-700 hover:bg-slate-700/50"
	variant="secondary"
	href="/"
>
	<House class="h-10 w-10" />
</Button>
<div class="relative flex h-full w-full flex-col items-center justify-center">
	<div class="w-[80%] max-w-96 rounded-lg bg-slate-700 p-4 ring-2 ring-slate-600">
		<h1 class="mb-4 w-full text-center text-4xl font-bold">Log In</h1>
		<a href="{PUBLIC_AUTH_URL}/oauth/github/login">
			<Button class="mb-1 w-full bg-slate-200">
				<MicrosoftLogo /> Microsoft
			</Button>
		</a>
		<div class="my-2 flex w-full items-center">
			<div class="h-0.5 w-full rounded-full bg-slate-500" />
			<p class="mx-2 text-[0.7rem] text-slate-300">OR</p>
			<div class="h-0.5 w-full rounded-full bg-slate-500" />
		</div>
		<form onsubmit={login}>
			<div class="mb-2">
				<Label class="text-lg ">Email / Username</Label>
				<Input bind:value={username} class="focusring !mt-1 rounded-lg bg-slate-800 text-base" />
			</div>
			<div class="mb-2">
				<Label class="text-lg ">Password</Label>
				<div class="relative">
					{#if passVisible}
						<Input
							bind:value={password}
							class="focusring !mt-1 rounded-lg bg-slate-800 text-base"
						/>
					{:else}
						<Input
							bind:value={password}
							class="focusring !mt-1 rounded-lg bg-slate-800 text-base"
							type="password"
						/>
					{/if}
					<Button
						class="focusring absolute right-0 top-0 h-10 w-10 rounded-lg p-2 hover:bg-slate-700/50"
						variant="ghost"
						onclick={() => {
							passVisible = !passVisible;
						}}
					>
						{#if passVisible}
							<EyeOff />
						{:else}
							<Eye />
						{/if}
					</Button>
				</div>
			</div>
			<Form.Button
				variant="secondary"
				class="focusring mt-2 w-full bg-purple-700 hover:bg-purple-800"
				>Log In
				{#if loading}
					<RefreshCw class="ml-2 animate-spin stroke-slate-100" />
				{/if}
			</Form.Button>
		</form>
	</div>
	<!-- <div
		class="mt-2 flex w-[80%] max-w-96 flex-col-reverse justify-between px-2 text-center md:flex-row"
	>
		<a href="/change-password" class="mt-1 underline md:mt-0">Forgot password?</a>
		<a href="/signup" class="mt-1 underline md:mt-0">Create an account</a>
	</div> -->
</div>
