<script lang="ts">
	import { page } from '$app/state';
	import type { PageProps } from './$types';
	import Button from '$lib/components/ui/button/button.svelte';
	import { goto } from '$app/navigation';
	import ChevronsLeft from 'lucide-svelte/icons/chevrons-left';
	import ConfigForm from './config-form.svelte';
	import { toast } from 'svelte-sonner';
	import Pause from 'lucide-svelte/icons/pause';
	import Trash2 from 'lucide-svelte/icons/trash-2';
	import ExternalLink from 'lucide-svelte/icons/external-link';
	let { data }: PageProps = $props();

	class MonitorStatus {
		static SUCCESS = 'SUCCESS';
		static ERROR = 'ERROR';
		static PAUSED = 'PAUSED';
	}
</script>

<Button
	variant="ghost"
	onclick={async () => await goto(`/monitors/${page.params.mid}`)}
	class="text-purple-500 hover:text-purple-600 hover:shadow-md"
>
	<ChevronsLeft strokeWidth={3} />
	<span class="-mx-1 text-base font-semibold italic">Go Back</span>
</Button>

<div>
	<div class="mx-10 mt-6 flex">
		<div>
			<h1 class="text-2xl font-medium italic">
				<span>Configure Monitor</span>
			</h1>
			<div class="text-md flex w-full items-center justify-start gap-3">
				<span
					class="capitalize"
					class:text-yellow-500={data.status == MonitorStatus.PAUSED}
					class:text-green-500={data.status == MonitorStatus.SUCCESS}
					class:text-red-500={data.status == MonitorStatus.ERROR}>{data.status.toLowerCase()}</span
				>
				<span class="text-2xl">&#183;</span>
				<span
					><a
						href={data.url}
						target="_blank"
						class="flex items-center gap-2 text-purple-600 hover:underline"
					>
						<span>{data.url}</span>
						{#if data.url}<ExternalLink size={14} />{/if}</a
					>
				</span>
			</div>
		</div>
	</div>

	<div class="flex flex-col gap-4 lg:mx-12">
		<div class=" mx-1 my-7 flex flex-col gap-4 lg:gap-10">
			<div class="flex flex-row items-end justify-end space-x-3">
				<Button
					variant="destructive"
					class="h-8"
					onclick={() => toast.success('Will mark this as deleted.')}><Trash2 /> Delete</Button
				>
				<Button
					variant="outline"
					class="h-8"
					onclick={() => toast.success('We will pause or un Pause')}
					><Pause />
					{#if data.paused}
						Unpause
					{:else}
						Pause
					{/if}
				</Button>
			</div>
			<div class="rounded-lg border shadow lg:mx-28">
				<ConfigForm {data} />
			</div>
		</div>
	</div>
</div>
