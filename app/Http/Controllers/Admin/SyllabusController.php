<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Services\CategoryService;
use Illuminate\Http\Request;

class SyllabusController extends Controller
{
    public function __construct(
        protected CategoryService $categoryService
    ) {}

    /**
     * Display a listing of the syllabus categories and subcategories.
     */
    public function index(Request $request)
    {
        $categories = $this->categoryService->getSyllabusTree();

        return $this->render('admin/syllabus/index', [
            'categories' => $categories,
        ]);
    }
}
