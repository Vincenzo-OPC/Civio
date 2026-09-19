<?php

declare(strict_types=1);

namespace App\Repositories;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

abstract class BaseRepository implements BaseRepositoryInterface
{
    public function __construct(
        protected Model $model
    ) {}

    public function all(array $columns = ['*'], array $relations = []): Collection
    {
        return $this->model->newQuery()->with($relations)->get($columns);
    }

    public function find(int|string $id, array $columns = ['*'], array $relations = []): ?Model
    {
        return $this->model->newQuery()->with($relations)->find($id, $columns);
    }

    public function findOrFail(int|string $id, array $columns = ['*'], array $relations = []): Model
    {
        return $this->model->newQuery()->with($relations)->findOrFail($id, $columns);
    }

    public function paginate(int $perPage = 15, array $columns = ['*'], array $relations = []): LengthAwarePaginator
    {
        return $this->model->newQuery()->with($relations)->paginate($perPage, $columns);
    }

    public function create(array $attributes): Model
    {
        return $this->model->newQuery()->create($attributes);
    }

    public function update(int|string $id, array $attributes): bool
    {
        $record = $this->find($id);

        return $record ? $record->update($attributes) : false;
    }

    public function delete(int|string $id): bool
    {
        $record = $this->find($id);

        return $record ? (bool) $record->delete() : false;
    }
}
