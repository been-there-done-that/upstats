<script lang="ts">
	import * as Form from '$lib/components/ui/form/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import { toast } from 'svelte-sonner';
	import { formSchema, type FormSchema } from './schema';
	import SuperDebug, { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { browser } from '$app/environment';

	let { data }: { data: { form: SuperValidated<Infer<FormSchema>> } } = $props();

	const form = superForm(data.form, {
		validators: zodClient(formSchema),
		onUpdated: ({ form: f }) => {
			if (f.valid) {
				toast.success(`You submitted ${JSON.stringify(f.data, null, 2)}`);
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

<form method="POST" use:enhance class="flex flex-col gap-3">
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

	<div class="flex items-center justify-evenly space-x-20">
		<Form.Field {form} name="method">
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

		<Form.Field {form} name="frequency">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label class="text-base font-semibold italic">Method</Form.Label>

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
	<Form.Button class="max-w-56 italic">Save</Form.Button>
</form>
