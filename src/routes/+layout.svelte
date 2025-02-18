<script lang="ts">
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import Sun from 'lucide-svelte/icons/sun';
	import Moon from 'lucide-svelte/icons/moon';
	import Logout from 'lucide-svelte/icons/log-out';
	import Activity from 'lucide-svelte/icons/activity';
	import Cog from 'lucide-svelte/icons/cog';
	import Calculator from 'lucide-svelte/icons/calculator';
	import Calendar from 'lucide-svelte/icons/calendar';
	import CreditCard from 'lucide-svelte/icons/credit-card';
	import Smile from 'lucide-svelte/icons/smile';
	import User from 'lucide-svelte/icons/user';
	import { afterNavigate, beforeNavigate } from '$app/navigation';

	import { onMount } from 'svelte';
	import * as Command from '$lib/components/ui/command/index.js';

	import { ModeWatcher, toggleMode } from 'mode-watcher';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.js';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import '../app.css';
	import { toast } from 'svelte-sonner';
	let { children } = $props();

	let logoutOpen = $state(false);
	let open = $state(false);

	onMount(() => {
		function handleKeydown(e: KeyboardEvent) {
			if (e.key === 'j' && (e.metaKey || e.ctrlKey)) {
				e.preventDefault();
				open = !open;
			}
		}

		document.addEventListener('keydown', handleKeydown);
		return () => {
			document.removeEventListener('keydown', handleKeydown);
		};
	});

	let loading = $state(false);

	beforeNavigate(async () => {
		loading = true;
	});

	afterNavigate(async () => {
		loading = false;
	});
</script>

{#if loading}
	<div class="loading-wrapper">
		<div class="loader"></div>
	</div>
{/if}

<Toaster position="top-right" />
<ModeWatcher />

<div class="flex h-screen flex-col items-center justify-center">
	<div
		class="flex w-full max-w-7xl items-center justify-end border-b border-black px-6 dark:border-gray-500"
	>
		<div class="my-3 flex w-full items-center justify-between">
			<a class="font-extrabold italic md:text-xl lg:text-2xl" href="/">UpStats ᯓ★</a>

			<p class="text-sm text-muted-foreground">
				Press
				<kbd
					class="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100"
				>
					<span class="text-xs">⌘</span>J
				</kbd>
			</p>
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
		<div class="mx-6 mb-24 mt-8 hidden flex-col items-center justify-between lg:col-span-2 lg:flex">
			<div class="flex flex-col gap-2">
				<Button variant="ghost" class="bg-gray-50 text-black" href="/">
					<Activity /> <span>Monitors</span>
				</Button>

				<Button variant="ghost" class="bg-gray-50 text-black" href="/">
					<Cog /> <span>Settings</span>
				</Button>
			</div>
			<div>
				<Button variant="destructive" onclick={() => (logoutOpen = true)}>
					<Logout class="text-black dark:text-white" /> <span>Logout</span>
				</Button>
			</div>
		</div>
		<div class="col-span-full border-l border-black dark:border-gray-500 lg:col-span-10">
			<div class="mt-9 lg:px-10">
				{@render children()}
			</div>
		</div>
	</div>
</div>

<!-- This will take care of the logout part -->
<AlertDialog.Root bind:open={logoutOpen}>
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
				onclick={() => [(logoutOpen = !logoutOpen), toast.error('We will logyou out...')]}
				>Confim</AlertDialog.Action
			>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

<Command.Dialog bind:open>
	<Command.Input placeholder="Type a command or search..." />
	<Command.List>
		<Command.Empty>No results found.</Command.Empty>
		<Command.Group heading="Suggestions">
			<Command.Item>
				<Calendar />
				<span>Calendar</span>
			</Command.Item>
			<Command.Item>
				<Smile />
				<span>Search Emoji</span>
			</Command.Item>
			<Command.Item>
				<Calculator />
				<span>Calculator</span>
			</Command.Item>
		</Command.Group>
		<Command.Separator />
		<Command.Group heading="Settings">
			<Command.Item>
				<User />
				<span>Profile</span>
				<Command.Shortcut>⌘P</Command.Shortcut>
			</Command.Item>
			<Command.Item>
				<CreditCard />
				<span>Billing</span>
				<Command.Shortcut>⌘B</Command.Shortcut>
			</Command.Item>
			<Command.Item>
				<Cog />
				<span>Settings</span>
				<Command.Shortcut>⌘S</Command.Shortcut>
			</Command.Item>
		</Command.Group>
	</Command.List>
</Command.Dialog>

<style>
	.loading-wrapper {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgb(82 78 78 / 80%);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
	}

	.loader {
		width: fit-content;
		font-weight: 800;
		white-space: pre;
		font-size: xxx-large;
		color: black;
		line-height: 1.2em;
		height: 1.2em;
		overflow: hidden;
	}

	.loader:before {
		content: 'Loading...\A⌰oading...\A⌰⍜ading...\A⌰⍜⏃ding...\A⌰⍜⏃⎅ing...\A⌰⍜⏃⎅⟟ng...\A⌰⍜⏃⎅⟟⋏g...\A⌰⍜⏃⎅⟟⋏☌...\A⌰⍜⏃⎅⟟⋏☌⟒..\A⌰⍜⏃⎅⟟⋏☌⟒⏁.\A⌰⍜⏃⎅⟟⋏☌⟒⏁⋔';
		white-space: pre;
		display: inline-block;
		animation: loadingAnim 1.6s infinite steps(11) alternate;
	}

	@keyframes loadingAnim {
		100% {
			transform: translateY(-100%);
		}
	}
</style>
