<script lang="ts">
	import type { Event } from '$lib/types';
	import { Clock, MapPin, Coins, Users } from 'lucide-svelte';
    import Button from './ui/button/button.svelte';

	export let submission: Event;
</script>

<div class="flex flex-col w-96 bg-slate-700 border-slate-600 border-2 p-4 gap-y-2 rounded-lg">
	<h1 class="flex h1 text-3xl font-bold truncate">{submission.title}</h1>
	<div class="flex gap-x-2">
		<Clock class="size-6 text-slate-400" />
		<p class="text-slate-400">
			{submission.start.toLocaleDateString('en-US')} - {submission.end.toLocaleDateString('en-US')}
		</p>
	</div>
	<div class="flex gap-x-2">
		<MapPin class="size-6 text-slate-400" />
		<p class="text-slate-400">{submission.location}</p>
	</div>
	<div class="flex gap-x-2">
		<Coins class="size-6 text-slate-400" />
		<p class="text-slate-400">{submission.price}</p>
	</div>
	<div class="flex gap-x-2">
		<Users class="size-6 text-slate-400" />
		<p class="text-slate-400">{submission.people}</p>
	</div>
	<div class="flex justify-between pt-2">
		<Button class="bg-purple-700 text-white text-lg p-6 hover:bg-purple-800">Edit</Button>
		<Button class="bg-slate-600 text-white text-lg p-6 hover:bg-slate-600/50">Awaiting Approvement</Button>
	</div>
</div>
