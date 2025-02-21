<script lang="ts">
	import * as Form from '$lib/components/ui/form/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import { toast } from 'svelte-sonner';
	import { formSchema, type FormSchema } from './schema';
	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { invalidateAll } from '$app/navigation';
	import { PUBLIC_BASE_URL } from '$env/static/public';

	let {
		data,
		closeCreate
	}: { data: { form: SuperValidated<Infer<FormSchema>> }; closeCreate: () => {} } = $props();

	const form = superForm(data.form, {
		validators: zodClient(formSchema),
		onUpdated: async ({ form: f }) => {
			if (f.valid) {
				const req = await fetch(`${PUBLIC_BASE_URL}/api/v1/event`, {
					body: JSON.stringify(f.data),
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					}
				});
				try {
					console.log(req.statusText);
					if (req.statusText == 'OK') {
						let res = await req.json();
						toast.success('Event Monitor Created...');
						closeCreate();
					} else {
						toast.error(`Failed to Save data ${await req.text()}`);
					}
				} catch (e) {
					toast.error(`Faileds to Save data ${e}`);
				}
				await invalidateAll();
			} else {
				toast.error('Please fix the errors in the form.');
			}
		},
		resetForm: false
	});

	const { form: formData, enhance } = form;

	const METHODS = ['GET', 'POST', 'PATCH', 'PUT'];

	const FREQUENCY = {
		'1 Minute': 60,
		'5 Minutes': 60 * 5,
		'15 Minutes': 60 * 15,
		'30 Minutes': 60 * 30,
		'1 Hour': 60 * 60,
		'12 Hours': 60 * 60 * 12,
		'24 Hours': 60 * 60 * 24
	};

	const REVERSED_FREQUENCY = Object.fromEntries(
		Object.entries(FREQUENCY).map(([key, value]) => [value, key])
	);
</script>

<form method="POST" use:enhance class="m-4 flex flex-col gap-3">
	<Form.Field {form} name="name">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label class="text-base font-semibold italic">Name</Form.Label>
				<Input {...props} bind:value={$formData.name} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<Form.Field {form} name="url">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label class="text-base font-semibold italic">Url</Form.Label>
				<Input {...props} bind:value={$formData.url} />
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<div class="flex flex-wrap items-center justify-center gap-3">
		<Form.Field {form} name="method" class="mx-6 w-full max-w-xs">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label class="text-base font-semibold italic">Method</Form.Label>
					<Select.Root type="single" bind:value={$formData.method} name={props.name}>
						<Select.Trigger {...props}>
							{$formData.method ? $formData.method : 'Select a method'}
						</Select.Trigger>
						<Select.Content>
							{#each METHODS as met}
								<Select.Item value={met} label={met} />
							{/each}
						</Select.Content>
					</Select.Root>
				{/snippet}
			</Form.Control>
			<Form.Description>HTTP Method used to make the request</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="frequency" class="mx-6 w-full max-w-xs">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label class="text-base font-semibold italic">Frequency</Form.Label>

					<Select.Root type="single" bind:value={$formData.frequency} name={props.name}>
						<Select.Trigger {...props}>
							<!-- Prefill: Show the string corresponding to the numeric value -->
							{$formData.frequency
								? Object.keys(FREQUENCY).find((key) => FREQUENCY[key] === $formData.frequency)
								: 'Select Frequency'}
						</Select.Trigger>
						<Select.Content>
							{#each Object.entries(FREQUENCY) as [f_str, f_num]}
								<Select.Item value={f_num} label={f_str} />
							{/each}
						</Select.Content>
					</Select.Root>
				{/snippet}
			</Form.Control>
			<Form.Description>How often you want to us to ping the API</Form.Description>
			<Form.FieldErrors />
		</Form.Field>
	</div>
	<div class="mt-6 flex justify-center">
		<Form.Button class="w-full max-w-56 italic">Save</Form.Button>
	</div>
</form>
