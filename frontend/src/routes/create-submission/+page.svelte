<script lang="ts">
	import type { PageData } from './$types';
	import SubmissionForm from '$lib/components/SubmissionForm.svelte';

	let { data }: { data: PageData } = $props();
</script>

<div class="flex w-full justify-center items-center pb-10">
	<SubmissionForm {data} />
</div>
