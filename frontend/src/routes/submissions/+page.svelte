<script lang="ts">
	import type { PageData } from './$types';
	import Submission from '$lib/components/Submission.svelte';
	import type { Event } from '$lib/types';
	import { onMount } from 'svelte';
	import ChevronLeft from 'lucide-svelte/icons/chevron-left';
	import ChevronRight from 'lucide-svelte/icons/chevron-right';
	import { MediaQuery } from 'svelte/reactivity';
	import * as Pagination from '$lib/components/ui/pagination/index.js';
	import Spinner from '$lib/components/Spinner.svelte';

	const isDesktop = new MediaQuery('(min-width: 768px)');

	const perPage = $derived(6);
	const siblingCount = $derived(isDesktop.current ? 1 : 0);

	let currentPage = $state(1);

	let submissions: Event[] = $state([]);
	const count = $derived(submissions.length);

	let roles: Promise<any>;
	onMount(async () => {
		const res = await fetch('https://0.0.0.0:8002/roles');
		
		roles = res.json();
		roles.then((data) => {
			console.log(data);
		});
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

		for (let i = 0; i < 100; i++) {
			submissions.push({
				title: `Event ${i + 3}`,
				start: new Date(),
				end: new Date(),
				location: `Location ${i + 3}`,
				price: 1000,
				people: 10
			});
		}
	});
</script>


{#await roles}
	<p>test</p>
	<div class="flex justify-center items-center h-full w-full bg-slate-100">
		<Spinner class="size-24" />
	</div>
{:then data}
	<p>{data}</p>
	<div class="grid grid-cols-3 gap-5 p-5">
		{#each submissions.slice((currentPage - 1) * perPage, (currentPage - 1) * perPage + perPage) as submission}
			<Submission {submission} />
		{/each}
	</div>

	<Pagination.Root
		{count}
		{perPage}
		{siblingCount}
		bind:page={currentPage}
		class="flex justify-end pb-10 h-full"
	>
		{#snippet children({ pages, currentPage })}
			<Pagination.Content>
				<Pagination.Item>
					<Pagination.PrevButton>
						<ChevronLeft class="size-4" />
						<span class="hidden sm:block">Previous</span>
					</Pagination.PrevButton>
				</Pagination.Item>
				{#each pages as page (page.key)}
					{#if page.type === 'ellipsis'}
						<Pagination.Item>
							<Pagination.Ellipsis />
						</Pagination.Item>
					{:else}
						<Pagination.Item>
							<Pagination.Link
								{page}
								isActive={currentPage === page.value}
								class="text-white data-[selected]:bg-slate-700"
							>
								{page.value}
							</Pagination.Link>
						</Pagination.Item>
					{/if}
				{/each}
				<Pagination.Item>
					<Pagination.NextButton>
						<span class="hidden sm:block">Next</span>
						<ChevronRight class="size-4" />
					</Pagination.NextButton>
				</Pagination.Item>
			</Pagination.Content>
		{/snippet}
	</Pagination.Root>
{:catch error}
	<p>Error loading roles: {error.message}</p>
{/await}
