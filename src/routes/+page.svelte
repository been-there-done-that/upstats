<script lang="ts">
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import Ellipsis from 'lucide-svelte/icons/ellipsis';
	import * as Table from '$lib/components/ui/table/index.js';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	import { cn } from '$lib/utils';

	const BEATS_ITEMS = 10;

	let selectedRowForDelete: null | any = $state(null);
	let open = $state(false);

	$effect(() => {
		open = !!selectedRowForDelete;
	});

	const invoices = [
		{
			id: '121212',
			name: 'Google',
			url: 'http://google.com',
			beats: [
				{ id: '1', date: '2025-02-15T10:27:01Z', status_code: 400 },
				{
					id: '2',
					date: '2025-02-15T10:28:01Z',
					status_code: 200
				},
				{
					id: '3',
					date: '2025-02-15T10:29:01Z',
					status_code: 200
				}
			],
			frequency: '5 Min'
		}
	];

	const BEATS_COLOR_MAPPING: { [key: number]: string } = {
		200: 'bg-green-400',
		201: 'bg-green-400',
		300: 'bg-green-400',
		400: 'bg-red-600',
		401: 'bg-red-600',
		402: 'bg-red-600',
		403: 'bg-red-600',
		404: 'bg-red-600',
		405: 'bg-red-600',
		500: 'bg-purple-500'
	};
</script>

<h1 class="text-2xl font-extrabold italic">Monitors</h1>

{#snippet Beats(invoice: any)}
	<div class="flex h-6 flex-row-reverse gap-1.5">
		{#each { length: BEATS_ITEMS } as _, idx}
			{@const value = invoice.beats[idx]}
			<Tooltip.Provider>
				<Tooltip.Root>
					<Tooltip.Trigger
						><div
							class={cn(
								'h-full w-1.5 rounded-md',
								BEATS_COLOR_MAPPING[value?.status_code] ?? 'bg-black/10 dark:bg-white/20'
							)}
						></div></Tooltip.Trigger
					>
					<Tooltip.Content
						class={BEATS_COLOR_MAPPING[value?.status_code] ?? 'bg-black dark:bg-white'}
					>
						<div
							class={cn(
								!value ? 'text-white dark:text-black' : 'text-black',
								'font-semibold italic'
							)}
						>
							{value?.date ?? 'Not Ran Yet'}{value ? ` - ${value.status_code}` : ''}
						</div>
					</Tooltip.Content>
				</Tooltip.Root>
			</Tooltip.Provider>
		{/each}
	</div>
{/snippet}

<div class="my-8 w-full rounded-lg border text-gray-500 shadow-md hover:text-black dark:text-white">
	<Table.Root>
		<Table.Header>
			<Table.Row>
				<Table.Head class="w-[30%] pl-5 text-left italic text-black dark:text-white"
					>Name</Table.Head
				>
				<Table.Head class="w-[30%] text-start italic text-black dark:text-white">URL</Table.Head>
				<Table.Head class="w-[20%] text-center italic text-black dark:text-white">Beats</Table.Head>
				<Table.Head class="w-[10%] text-center italic text-black dark:text-white"
					>Frequency</Table.Head
				>
				<Table.Head class="w-[10%] text-center italic text-black dark:text-white">Action</Table.Head
				>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each invoices as invoice, i (i)}
				<Table.Row class="group">
					<Table.Cell
						class=" w-[30%] pl-5 text-left text-gray-500 group-hover:text-black dark:text-white"
						>{invoice.name}</Table.Cell
					>
					<Table.Cell
						class=" -p-2 w-[30%] text-start text-gray-500 group-hover:text-black dark:text-white"
						>{invoice.url}</Table.Cell
					>
					<Table.Cell
						class="grid  w-full place-items-center text-gray-500 group-hover:text-black dark:text-white"
					>
						<div>
							{@render Beats(invoice)}
						</div>
					</Table.Cell>
					<Table.Cell
						class=" -p-2 w-[10%] text-center text-gray-500 group-hover:text-black dark:text-white"
						>{invoice.frequency}</Table.Cell
					>
					<Table.Cell class=" -p-2 w-[10%] text-center text-black dark:text-white">
						<DropdownMenu.Root>
							<DropdownMenu.Trigger class={buttonVariants({ variant: 'ghost', size: 'icon' })}
								><Ellipsis /></DropdownMenu.Trigger
							>
							<DropdownMenu.Content>
								<DropdownMenu.Group>
									<DropdownMenu.Item>
										<Button variant="ghost" class="h-5" href="/somewhere">Configure</Button>
									</DropdownMenu.Item>
									<DropdownMenu.Separator />
									<DropdownMenu.Item class="flex items-center justify-center">
										<Button
											variant="ghost"
											class="h-5 w-full"
											onclick={() => (selectedRowForDelete = invoice)}
										>
											Delete
										</Button>
									</DropdownMenu.Item>
								</DropdownMenu.Group>
							</DropdownMenu.Content>
						</DropdownMenu.Root>
					</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>

<!-- This will take care of the logout part -->
<AlertDialog.Root bind:open>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete your account and remove your data
				from our servers.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action
				class={buttonVariants({ variant: 'destructive' })}
				onclick={() => [(open = !open), toast.error('We will Delete This Row from database...')]}
				>Confim</AlertDialog.Action
			>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
