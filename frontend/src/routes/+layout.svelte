<script lang="ts">
	import { page } from '$app/state';
	import { Button } from '$lib/components/ui/button';
	import '../app.css';
	let { children } = $props();

	let loggedIn = false;

	const navItems = [
		{ name: 'Submissions', href: '/submissions' },
		{ name: 'Create Submission', href: '/create-submission' },
		{ name: 'Reviewed Submissions', href: '/reviewed-submissions' },
		{ name: 'Review', href: '/review' }
	];

	const excludeRoutes = ['/login', '/register'];
</script>

<div class="h-full w-full flex flex-col">
	{#if !excludeRoutes.includes(page.url.pathname)}
		<nav class="h-16 border-b-2 border-slate-700 p-2 flex items-center justify-between">
			<div class="flex items-center space-x-2">
				<Button
					href="/"
					variant="secondary"
					class="bg-slate-800 hover:bg-slate-700 h-12 px-3 text-2xl">VM</Button
				>
				{#each navItems as item}
					{#if page.url.pathname === item.href}
						<Button
							href={item.href}
							variant="secondary"
							class="border-2 border-slate-700 bg-slate-700 hover:bg-slate-700 !mr-2"
							>{item.name}</Button
						>
					{:else}
						<Button href={item.href} variant="secondary" class="border-2 border-slate-700 !mr-2"
							>{item.name}</Button
						>
					{/if}
				{/each}
			</div>
			<div>
				{#if loggedIn}
					<div class="rounded-full bg-slate-700 h-10 w-auto aspect-square mr-1"></div>
				{:else}
					<Button href="/login" class="bg-purple-700 hover:bg-purple-800 text-slate-100"
						>Log In</Button
					>
				{/if}
			</div>
		</nav>
	{/if}

	<div class="h-full w-full p-8 flex flex-col items-center">
		{@render children()}
	</div>
</div>
