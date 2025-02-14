<script lang="ts">
	// import '@fontsource/ibm-plex-mono';
	// import '@fontsource/ibm-plex-sans-condensed';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';
	import { ModeWatcher, toggleMode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button/index.js';
	import '../app.css';
	let { children } = $props();
</script>

<Toaster position="top-right" />
<ModeWatcher />

<div class="flex h-screen flex-col items-center justify-center">
	<div
		class="flex w-full max-w-6xl items-center justify-end border-b border-black px-6 dark:border-gray-500"
	>
		<div class="my-3 flex w-full items-center justify-between">
			<h2 class="text-2xl font-extrabold italic">UpStats ᯓ★</h2>

			<Button onclick={toggleMode} variant="outline" size="icon">
				<Sun
					class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
				/>
				<Moon
					class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
				/>
				<span class="sr-only">Toggle theme</span>
			</Button>
		</div>
	</div>
	<div class="grid h-full w-full max-w-6xl grid-flow-col grid-cols-12">
		<div class="col-span-2">a</div>
		<div class="col-span-10 border-l border-black dark:border-gray-500">
			<div class="m-6">
				{@render children()}
			</div>
		</div>
	</div>
</div>
