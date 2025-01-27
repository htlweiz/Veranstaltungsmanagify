<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<div class="h-full w-full flex flex-col">
	<nav class="h-16 border-b-2 border-slate-600 p-2 flex items-center">nav</nav>
	<div class="h-full">
		{@render children()}
	</div>
</div>
