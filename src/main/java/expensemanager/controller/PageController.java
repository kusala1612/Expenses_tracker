package expensemanager.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping("/home")
    public String home() {
        return "home";
    }

    @GetMapping("/income-page")
    public String incomePage() {
        return "income";
    }

    @GetMapping("/expenditure-page")
    public String expenditurePage() {
        return "expenditure";
    }

    @GetMapping("/view-expenditure")
    public String viewExpenditure() {
        return "view-expenditure";
    }

    @GetMapping("/monthly-graph")
    public String monthlyGraph() {
        return "monthly-graph";
    }

    @GetMapping("/yearly-graph")
    public String yearlyGraph() {
        return "yearly-graph";
    }

    @GetMapping("/category-wise")
    public String categoryWise() {
        return "category-wise";
    }

    @GetMapping("/balance-page")
    public String balancePage() {
        return "balance";
    }

    @GetMapping("/pdf-page")
    public String pdfPage() {
        return "pdf-report";
    }
    @GetMapping("/view-income")
public String viewIncome() {
    return "view-income";
}
}