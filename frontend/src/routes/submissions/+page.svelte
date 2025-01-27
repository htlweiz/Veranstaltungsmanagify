<script lang="ts">
	import type { PageData } from './$types';
	import Submission from '$lib/components/Submission.svelte';
	import type { Event } from '$lib/types';
	import { onMount } from 'svelte';

	let submissions: Event[] = [];
	onMount(async () => {
		submissions = [
			{
				title: 'Event 1',
				start: new Date(),
				end: new Date(),
				location: 'Location 1',
				price: 2500,
				people: 24
			},
			{
				title: 'Event 2',
				start: new Date(),
				end: new Date(),
				location: 'Location 2',
				price: 300,
				people: 3
			}
		];
	});
</script>

<div class="flex flex-wrap gap-5 p-5">
	{#each submissions as submission}
		<Submission {submission} />
	{/each}
</div>
