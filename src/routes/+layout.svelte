<script lang="ts">
		// import '@fontsource/ibm-plex-mono';
		// import '@fontsource/ibm-plex-sans-condensed';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import Sun from "lucide-svelte/icons/sun";
	import Moon from "lucide-svelte/icons/moon";
	import { ModeWatcher, toggleMode } from "mode-watcher";
	import { Button } from "$lib/components/ui/button/index.js";
	import '../app.css';
	let { children } = $props();
</script>

<Toaster position="top-right" />
<ModeWatcher />


<div class="flex items-center justify-center flex-col h-screen">
	<div class="w-full max-w-6xl border-b border-black dark:border-gray-500 flex justify-end items-center px-6">

		<div class="my-3 flex justify-between items-center w-full">
			
			<h2 class="font-extrabold text-2xl italic"> UpStats ᯓ★</h2>

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
	<div class="grid grid-cols-12 grid-flow-col w-full max-w-6xl h-full">
		<div class="col-span-2">
			a
		</div>
		<div class="col-span-10 border-l border-black dark:border-gray-500">
			<div class="m-6">
			{@render children()}
		</div>
		</div>
	</div>
</div>



