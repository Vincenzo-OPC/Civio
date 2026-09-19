<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Category;
use Illuminate\Http\Request;

class SyllabusController extends Controller
{
    /**
     * Display a listing of the syllabus categories and subcategories.
     */
    public function index(Request $request)
    {
        $categories = Category::with('subcategory')->orderBy('name')->get();

        return $this->render('admin/syllabus/index', [
            'categories' => $categories,
        ]);
    }
}
