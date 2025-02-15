<script lang="ts">
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';
	import Logout from 'lucide-svelte/icons/log-out';
	import Activity from 'lucide-svelte/icons/activity';
	import Settings from 'lucide-svelte/icons/settings';

	import { ModeWatcher, toggleMode } from 'mode-watcher';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.js';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import '../app.css';
	import { toast } from 'svelte-sonner';
	let { children } = $props();

	let open = $state(false);
</script>

<Toaster position="top-right" />
<ModeWatcher />

<div class="flex h-screen flex-col items-center justify-center">
	<div
		class="flex w-full max-w-7xl items-center justify-end border-b border-black px-6 dark:border-gray-500"
	>
		<div class="my-3 flex w-full items-center justify-between">
			<h2 class="lg:text-2xl md:text-xl font-extrabold italic">UpStats ᯓ★</h2>

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
	<div class="grid h-full w-full max-w-7xl grid-flow-col grid-cols-12">
		<div class="lg:col-span-2 mx-6 mb-24 mt-8 lg:flex flex-col items-center justify-between hidden">
			<div class="flex flex-col gap-2">
				<Button variant="ghost" class="bg-gray-50 text-black" href="/">
					<Activity /> <span>Monitors</span>
				</Button>

				<Button variant="ghost" class="bg-gray-50 text-black" href="/">
					<Settings /> <span>Settings</span>
				</Button>
			</div>
			<div>
				<Button variant="destructive" onclick={() => (open = true)}>
					<Logout class="text-black dark:text-white" /> <span>Logout</span>
				</Button>
			</div>
		</div>
		<div class="lg:col-span-10 border-l border-black dark:border-gray-500 col-span-full">
			<div class="lg:m-6 m-3">
				{@render children()}
			</div>
		</div>
	</div>
</div>

<!-- This will take care of the logout part -->
<AlertDialog.Root bind:open>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This Action will Log You of out your account.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action
				class={buttonVariants({ variant: 'destructive' })}
				onclick={() => [(open = !open), toast.error('We will logyou out...')]}
				>Confim</AlertDialog.Action
			>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
