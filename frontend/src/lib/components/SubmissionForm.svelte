<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator/index.js';

	import { type SuperValidated, type Infer, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { submissionSchema, type SubmissionSchema } from '$lib/schemas';

	let { data }: { data: { form: SuperValidated<Infer<SubmissionSchema>> } } = $props();
	const form = superForm(data.form, {
		dataType: 'json',
		validators: zodClient(submissionSchema)
	});

	const { form: formData, enhance } = form;
</script>

<div class="flex p-5 bg-slate-700 border-slate-600 border-2 rounded-lg w-1/2">
	<form
		method="POST"
		use:enhance
		class="flex flex-col space-y-4 justify-center items-center w-full"
	>
		<h1 class="text-3xl font-bold">New Submission</h1>
		<Separator class="bg-slate-600 w-2/3" />

		<div class="flex w-full justify-between items-center">
			<div class="flex flex-col space-y-4 w-1/2 justify-center items-start">
				<Form.Field {form} name="start" class="w-full">
					<Form.Control>
						{#snippet children({ props })}
							<Form.Label>Start Date</Form.Label>
							<Input
								{...props}
								type="date"
								class="bg-slate-600 border-slate-500"
								bind:value={$formData.start}
							/>
						{/snippet}
					</Form.Control>
				</Form.Field>

				<Form.Field {form} name="end" class="w-full">
					<Form.Control>
						{#snippet children({ props })}
							<Form.Label>End Date</Form.Label>
							<Input
								{...props}
								type="date"
								class="bg-slate-600 border-slate-500"
								bind:value={$formData.end}
							/>
						{/snippet}
					</Form.Control>
				</Form.Field>
			</div>
			<div class="flex flex-col space-y-4 justify-center items-start w-1/3">
				<Form.Field {form} name="total_costs" class="w-full">
					<Form.Control>
						{#snippet children({ props })}
							<Form.Label>Total Costs</Form.Label>
							<Input
								{...props}
								type="number"
								class="bg-slate-600 border-slate-500"
								bind:value={$formData.total_costs}
							/>
						{/snippet}
					</Form.Control>
				</Form.Field>

				<Form.Field {form} name="transportation_costs" class="w-full">
					<Form.Control>
						{#snippet children({ props })}
							<Form.Label>Transportation Costs</Form.Label>
							<Input
								{...props}
								type="number"
								class="bg-slate-600 border-slate-500"
								bind:value={$formData.transportation_costs}
							/>
						{/snippet}
					</Form.Control>
				</Form.Field>
			</div>
		</div>

		<Separator class="bg-slate-600 w-2/3" />

		<div class="flex flex-col space-y-4 w-full justify-between items-center">
			<h2 class="h2 items-end w-full text-2xl font-bold">Participants</h2>
			<div class="flex space-x-4 w-full justify-start items-center">
				<fieldset>
					{#each $formData.teachers as teacher, index}
						<Input type="text" bind:value={$formData.teachers[index]} />
					{/each}
					<Button
						type="button"
						class="bg-slate-600 text-white text-lg p-6 hover:bg-slate-500"
						on:click={() => $formData.teachers.push('')}>Add Teacher</Button
					>
				</fieldset>
				<fieldset>
					{#each $formData.students as student, index}
						<Input type="text" bind:value={$formData.students[index]} />
					{/each}
					<Button
						type="button"
						class="bg-slate-600 text-white text-lg p-6 hover:bg-slate-500"
						on:click={() => $formData.students.push('')}>Add Student</Button
					>
				</fieldset>
			</div>
		</div>

		<Separator class="bg-slate-600 w-2/3" />

		<h2 class="h2 items-end w-full text-2xl font-bold">Address</h2>
		<fieldset class="flex flex-col w-full space-y-3">
			<div class="flex w-full justify-between items-start space-x-3">
				<div class="flex flex-col space-y-2 justify-center items-start w-1/2">
					<Form.Field {form} name="address" class="w-full">
						<Form.Control>
							{#snippet children({ props })}
								<Form.Label>Country</Form.Label>
								<Input
									{...props}
									type="text"
									class="bg-slate-600 border-slate-500"
									bind:value={$formData.address.country}
								/>
							{/snippet}
						</Form.Control>
					</Form.Field>

					<Form.Field {form} name="address" class="w-full">
						<Form.Control>
							{#snippet children({ props })}
								<Form.Label>State</Form.Label>
								<Input
									{...props}
									type="text"
									class="bg-slate-600 border-slate-500"
									bind:value={$formData.address.state}
								/>
							{/snippet}
						</Form.Control>
					</Form.Field>
				</div>
				<div class="flex flex-col space-y-2 justify-center items-start w-1/2">
					<Form.Field {form} name="address" class="w-full">
						<Form.Control>
							{#snippet children({ props })}
								<Form.Label>City</Form.Label>
								<Input
									type="text"
									{...props}
									class="bg-slate-600 border-slate-500"
									bind:value={$formData.address.street}
								/>
							{/snippet}
						</Form.Control>
					</Form.Field>

					<Form.Field {form} name="address" class="w-full">
						<Form.Control>
							{#snippet children({ props })}
								<Form.Label>Street</Form.Label>
								<Input
									type="text"
									{...props}
									class="bg-slate-600 border-slate-500"
									bind:value={$formData.address.street}
								/>
							{/snippet}
						</Form.Control>
					</Form.Field>

					<Form.Field {form} name="address" class="w-full">
						<Form.Control>
							{#snippet children({ props })}
								<Form.Label>Zip</Form.Label>
								<Input
									{...props}
									type="text"
									class="bg-slate-600 border-slate-500"
									bind:value={$formData.address.city}
								/>
							{/snippet}
						</Form.Control>
					</Form.Field>
				</div>
			</div>
		</fieldset>

		<Separator class="bg-slate-600 w-2/3" />

		<Label>Curriculum Reference</Label>
		<Textarea
			type="text"
			bind:value={$formData.curriculum_ref}
			class=" bg-slate-600 border-slate-500"
		/>

		<Label>Parental Info</Label>
		<Textarea class="bg-slate-600 border-slate-500" bind:value={$formData.parental_info} />

		<div class="flex justify-end w-full pt-5">
			<Form.Button class="bg-purple-700 text-white text-lg p-6 hover:bg-purple-800"
				>Submit</Form.Button
			>
		</div>
	</form>
</div>
